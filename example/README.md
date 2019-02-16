# Terraform provision gitlab

#### Requirements

- https://www.terraform.io/
- https://www.terraform.io/docs/providers/do/index.html
- https://github.com/radekg/terraform-provisioner-ansible
- environment variable DIGITALOCEAN_TOKEN

#### Use

    terraform init
    terraform apply

#### Output

- token
- domain
- root password (can be changed in gitlab.tf)
