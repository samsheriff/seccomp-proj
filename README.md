<h2 align="center"> Technical assignment by Security Compass</h1>

This project deploys a Python application on a Kubernetes cluster on Amazon's AWS EKS.
The simple Python application is architected with Microservices in mind.

This is the roadmap I had in mind when I started working on this assignment:
- Write the Python application in a way that it's made of two small services that communicate through network (TCP ports).
- EKS Cluster, VPC, Subnets, IAM details, Networking details and etc. needs to be provisioned by Terraform on AWS
- Deploy a Jenkins instance on an EC2 box and create a pipeline to do the k8s deployment and also the build and deployment of our microservices on the EKS cluster. This step can be done in a way to be a show-off for a DevOps engineer :) I will use Helm for Jenkins deployment (helm_release.tf) while all the configuration is already set in (jenkins_values.yaml). This was heavily inspired by Jenkins' Help Charts docs: https://github.com/jenkinsci/helm-charts/tree/main/charts/jenkins
- Our Python application will be deployed on our EKS cluster from this Jenkins instance.

This next phase considers you have all the basic requirements in place:
* AWS Admin access
* AWS CLI be installed and properly configured
* kubectl, Docker and Terraform are installed

## Create the EKS cluster using Terraform
We will be using a few Terraform providers for this. We will also take advantage of some prebuilt Terraform modules, like  [AWS VPC Terraform Module](https://github.com/terraform-aws-modules/terraform-aws-vpc) and [Amazon EKS Blueprints for Terraform](https://github.com/aws-ia/terraform-aws-eks-blueprints).

Each of the files in the repo, do different things and when needed, in-line documentation has been provided.

We need a VPC, subnets, route tables, and other networking bits. We will use the vpc module from the *[terraform-aws-modules](https://github.com/terraform-aws-modules)* repository. This module is a wrapper around the AWS VPC module. It makes it easier to configure VPCs and all the other required networking resources. In more details, we will create *([vpc.tf](https://github.com/samsheriff/seccomp-proj/blob/main/vpc.tf))*:
* A new VPC, three private subnets, and three public subnets
* Internet gateway and NAT gateway for the public subnets
* and AWS routes for the gateways, public/private route tables, and route table associations

Now that we have the networking part done, we can build configurations for the EKS cluster and its add-ons. We will use the `eks_blueprints` module from [terraform-aws-eks-blueprints](https://aws-ia.github.io/terraform-aws-eks-blueprints/v4.0.9/), which is a wrapper around the [terraform-aws-modules](https://github.com/terraform-aws-modules) and provides additional modules to configure EKS add-ons *([eks-cluster.tf](./eks-cluster.tf))*. In following will be created:
* EKS Cluster Control plane with one managed node group and [fargate profile](https://docs.aws.amazon.com/eks/latest/userguide/fargate-profile.html)
* Cluster and node security groups and rules, IAM roles and policies required
* and AWS Key Management Service (KMS) configuration.

To start provisioning the cluster:
```
# download modules and providers. Initialize state.
terraform init
# see a preview of what will be done
terraform plan
```
After reviewing everything and also making sure about access keys (`aws config`), we can apply the changes:

`terraform apply`

After a few minutes, our cluster should be ready and it can be confirmed by running the following command:

`kubectl get nodes`
