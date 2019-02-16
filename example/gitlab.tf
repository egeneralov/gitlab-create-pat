provider "digitalocean" {}


variable "password" {
  default = "PassW@rd123"
}


resource "digitalocean_droplet" "gitlab" {
  image = "debian-9-x64"
  name = "gitlab"
  region = "lon1"
  size = "s-2vcpu-2gb"
  private_networking = true
  ssh_keys = [
    "98:72:1e:a6:f5:4c:92:b0:92:67:7c:f4:11:2c:19:e5"
  ]

  connection {
    user = "root"
    type = "ssh"
    private_key = "${file(pathexpand("~/.ssh/id_rsa"))}"
    timeout = "2m"
  }

  provisioner "remote-exec" {
    inline = [
      "apt-get update -qq",
      "apt-get -yqq install python-pip",
      "pip install -U pip six setuptools"
    ]
  }

  provisioner "local-exec" {
    command = "echo"
  }

  provisioner "remote-exec" {
    inline = [
      "pip install ansible",
      "ansible-galaxy install egeneralov.gitlab",
    ]
  }

  provisioner "ansible" {
    plays {
      playbook = {
        file_path = "gitlab.yml"
      }
      enabled = true
      diff = false
      extra_vars = {
        domain = "${digitalocean_droplet.gitlab.ipv4_address}.xip.io"
        root_password = "${var.password}"
      }
    }
    ansible_ssh_settings {
      connect_timeout_seconds = 10
      connection_attempts = 10
      ssh_keyscan_timeout = 60
    }
    remote {
      use_sudo = false
      skip_install = true
      skip_cleanup = true
    }
  }

}


data "external" "token" {
  program = ["bash", "${path.root}/pat.sh"]
  query = {
    domain = "http://${digitalocean_droplet.gitlab.ipv4_address}.xip.io"
    user = "root"
    password = "${var.password}"
  }
  depends_on = [
    "digitalocean_droplet.gitlab"
  ]
}


output "token" { value = "${data.external.token.result["token"]}" }
output "domain" { value = "${digitalocean_droplet.gitlab.ipv4_address}.xip.io" }
output "password" { value = "${var.password}" }
