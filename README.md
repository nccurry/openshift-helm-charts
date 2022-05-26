
## Deploy

### Install the ArgoCD community operator
```shell
helm install argocd-operator ./argocd-operator --namespace argocd-operator --create-namespace --wait
```

### Deploy an ArgoCD instance
```shell
helm install argocd ./argocd-instance --namespace argocd --create-namespace --wait -f ./argocd-instance/values-<environment>.yaml
```

## Teardown

## Remove the ArgoCD instance
```shell 
helm uninstall argocd --namespace argocd --wait
oc delete namespace argocd
```

## Remove the ArgoCD community operator
```shell 
helm uninstall argocd-operator --namespace argocd-operator --wait
oc delete namespace argocd-operator
```
