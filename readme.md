Notes:
. This application assumes the GITHUB_TOKEN is being store as a environment variable.
. For this specific application it doesn't make sense to use a token as a user login would make more sense to manage accesses/permissions.
. The tests being made have the responses being mocked which also doesn't make any sense other than to make them as the excercise/test that this is.

- To create the secret for your GitHub token in minikube, run:
kubectl create secret generic github-token --from-literal=token=GITHUB_TOKEN

- Considerations
Secrets Management: Always keep sensitive data (like GITHUB_TOKEN) out of version control, using environment variables and Kubernetes secrets.
Tests: Add tests that check of DEV or PROD environment flag and change behaviour accordingly
Data to add to ENV: Stuff like the Github Rep url, environment flag and so on

- Best practices that should be done:
. Add a formater like Black
. Test coverage, usually around 70% or more

