# ArgoCD App of Apps

An example of the ArgoCD App of Apps pattern

```shell
helm install argocd-app-of-apps ./ --namespace openshift-gitops --create-namespace --wait -f values.yaml
```