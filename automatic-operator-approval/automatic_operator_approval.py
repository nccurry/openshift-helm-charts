#!/usr/bin/python3

import re
from kubernetes import client
from kubernetes.client.rest import ApiException

with open("/var/run/secrets/kubernetes.io/serviceaccount/token") as tokenFile:
    api_key = tokenFile.readline().rstrip()  # rstrip removes the newline

configuration = client.Configuration()
configuration.api_key['authorization'] = 'Bearer ' + api_key
configuration.host = 'https://kubernetes.default.svc'
configuration.ssl_ca_cert = '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'

with client.ApiClient(configuration) as api_client:
    api_client = client.CustomObjectsApi(api_client)

    try:
        get_install_plans = api_client.list_cluster_custom_object(group="operators.coreos.com", version="v1alpha1", plural="installplans")
        get_subscriptions = api_client.list_cluster_custom_object(group="operators.coreos.com", version="v1alpha1", plural="subscriptions")

        starting_csvs = []
        for subscription in get_subscriptions['items']:
            if 'startingCSV' in subscription['spec']:
                starting_csvs.append(subscription['spec']['startingCSV'])

        print('\nChecking for unapproved InstallPlans\nHere are the cluster Subscription starting CSVs')
        for starting_csv in starting_csvs:
            print('  %s' % starting_csv)

        if len(get_install_plans['items']) == 0:
            print('No unapproved InstallPlans')

        for install_plan in get_install_plans['items']:
            if not install_plan['spec']['approved']:
                print('\n  Found unapproved InstallPlan %s, checking if it should be approved' % install_plan['metadata']['name'])

                # We're going to loop through every clusterServiceVersionName in the InstallPlan
                # and find the associated Subscription startingCSV. Then we're going to use a little
                # regex magic to compare the strings by stripping all non-alphanumeric characters out
                # turning 'elasticsearch-operator.5.2.2-21' into 'elasticsearchoperator52221'
                # and checking which is bigger. In most cases a string like elasticsearchoperator53221 will be bigger
                # than elasticsearchoperator52221, which lets us know we can upgrade.
                # [^.]* captures everything up to a '.' so 'amqstreams' from 'amqstreams.v1.8.1'
                # \W+ matches anything that is not a 'word' character so '.', '-', etc
                approve_install_plan = True
                for cluster_service_version_name in install_plan['spec']['clusterServiceVersionNames']:
                    operator_name_search_csvn = re.search(r'[^.]*', cluster_service_version_name)

                    for starting_csv in starting_csvs:
                        operator_name_search_scsv = re.search(r'[^.]*', starting_csv)

                        if operator_name_search_csvn[0] == operator_name_search_scsv[0]:
                            operator_version_csvn = re.sub(r'\W+', '', cluster_service_version_name)
                            operator_version_scsv = re.sub(r'\W+', '', starting_csv)
                            if operator_version_csvn > operator_version_scsv:
                                approve_install_plan = False
                                print('    startingCSV %s is older than clusterServiceVersionName %s, cannot approve InstallPlan' % (starting_csv, cluster_service_version_name))
                            else:
                                print('    startingCSV %s is newer or equal to clusterServiceVersionName %s' % (starting_csv, cluster_service_version_name))

                if approve_install_plan:
                    print('    All clusterServiceVersionNames in InstallPlan %s are older or equal to their Subscription startingCSV, approving InstallPlan' % install_plan['metadata']['name'])
                    body = {
                        'spec': {
                            'approved': True
                        }
                    }
                    response = api_client.patch_namespaced_custom_object(
                        group="operators.coreos.com",
                        version="v1alpha1",
                        plural="installplans",
                        name=install_plan['metadata']['name'],
                        namespace=install_plan['metadata']['namespace'],
                        body=body
                    )

    except ApiException as e:
        print("Exception when calling OpenShift API: %s\n" % e)
        exit(1)





