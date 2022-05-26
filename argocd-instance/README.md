# ArgoCD App of Apps

An example of the ArgoCD App of Apps pattern

```shell
helm install argocd-instance ./ --namespace argocd --create-namespace --wait -f values-example.yaml
```