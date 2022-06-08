# OKD / OpenShift ArgoCD

## Deploy

### Set environment
```shell
K8S_ENVIRONMENT=environment
```

### Install the ArgoCD community operator or the OpenShift GitOps operator
```shell
# ArgoCD
helm install argocd-operator ./argocd-operator --namespace argocd-operator --create-namespace --wait

# OpenShift GitOps
helm install openshift-gitops-operator ./openshift-gitops-operator --namespace openshift-gitops-operator --create-namespace --wait
```

### Deploy an ArgoCD instance (not needed with the openshift-gitops operator)
```shell
helm install argocd ./argocd-instance --namespace openshift-gitops --create-namespace --wait -f ./argocd-instance/values-${K8S_ENVIRONMENT}.yaml
```

### Deploy the app-of-apps chart
```shell
helm install argocd ./app-of-apps --namespace openshift-gitops --wait -f ./app-of-apps/values-${K8S_ENVIRONMENT}.yaml
```

## Teardown

## Remove the ArgoCD instance
```shell 
helm uninstall argocd --namespace argocd --wait
oc delete namespace openshift-gitops
```

## Remove the ArgoCD community operator
```shell 
helm uninstall argocd-operator --namespace argocd-operator --wait
oc delete namespace argocd-operator
```

## Remove the OpenShift GitOps operator
```shell 
helm uninstall openshift-gitops-operator --namespace openshift-gitops-operator --wait
oc delete namespace openshift-gitops-operator
oc delete namespace openshift-gitops
```