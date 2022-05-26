# ArgoCD Operator

Install the ArgoCD operator

```shell
helm install argocd-operator ./argocd-operator --namespace argocd --create-namespace --wait -f values-<environment>.yaml
```