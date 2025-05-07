- To create the secret for your GitHub token in minikube, run:
kubectl create secret generic github-token --from-literal=token=GITHUB_TOKEN

- Considerations
Secrets Management: Always keep sensitive data (like GITHUB_TOKEN) out of version control, using environment variables and Kubernetes secrets.
Tests: Add tests that check of DEV or PROD environment flag and change behaviour accordingly
Data to add to ENV: Stuff like the Github Rep url, environment flag and so on

- Best practices that should be done:
. Add a formater like Black
. Test coverage, usually around 70% or more

