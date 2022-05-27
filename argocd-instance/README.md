# ArgoCD App of Apps

An example of the ArgoCD App of Apps pattern

```shell
K8S_ENVIRONMENT=environment
helm install argocd-instance ./ --namespace openshift-gitops --create-namespace --wait -f values-${K8S_ENVIRONMENT}.yaml
```