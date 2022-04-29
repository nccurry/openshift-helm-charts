## Openshift Image Registry Helm chart

This Helm chart supports configuration of the Openshift [Image Registry](https://docs.openshift.com/container-platform/latest/registry/configuring-registry-operator.html). Not all parameters supported by image registry operator are supported by this chart.

## Parameters

### Required parameters

The chart does not have any required parameters. See the table below for default values.

| Name | Default | Description |
|------|---------|-------------|
| defaultRoute | `false` | Determines whether or not an external route is defined using the default hostname. If enabled, the route uses re-encrypt encryption. |
| logLevel | `Normal` | Sets log level of the registry instance. Supported values are: `Normal`, `Debug`, `Trace` & `TraceAll` |
| managementState | `Managed` | Determines whether or not the operator should update the registry as the resources are updated. Supported values are: `Managed`, `Unmanaged` & `Removed`. |
| replicaCount | `1` | Replica count for the registry. |
| nodeSelector | `node-role.kubernetes.io/infra: ""` | Select the node(s) where the registry pod(s) will run |
| tolerations | `[{"key":"infra","value":"reserved","effect":"NoExecute"},{"key":"infra","value":"reserved","effect":"NoSchedule"}]` | The tolerations for the registry pods. |
| customRoutes.enabled | `false` | Determines wheter or not to create additional routes for the registry. |
| customRoutes.routes | N/A | Array of additional routes to create. You provide the hostname and certificate for the route. |

### Optional parameters

See `values.yaml` for optional parameters and defaults.

## ArgoCD application

This Day2 item can easily be consumed and applied by an ArgoCD instance.
```bash
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: openshift-image-registry
  namespace: argocd
spec:
  destination:
    server: https://kubernetes.default.svc
  project: default
  source:
    helm:
      parameters:
      - name: replicaCount
        value: "2"
    path: day2ops/openshift-image-registry
    repoURL: https://git.delta.com/openshift/operations.git
    targetRevision: HEAD
  syncPolicy:
    automated:
      selfHeal: true
      prune: false
```
