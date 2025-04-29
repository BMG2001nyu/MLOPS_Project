provider "openstack" {
  auth_url    = var.auth_url
  tenant_name = var.tenant_name
  user_name   = var.user_name
  password    = var.password
  region      = var.region
  domain_name = var.domain_name
}

resource "openstack_compute_instance_v2" "controller" {
  name            = "transcept-controller"
  image_name      = "Ubuntu 22.04"
  flavor_name     = "m1.medium"
  key_pair        = var.key_pair
  security_groups = ["default"]

  network {
    name = var.network
  }
}

resource "openstack_compute_instance_v2" "gpu1" {
  name            = "transcept-gpu1"
  image_name      = "Ubuntu 22.04"
  flavor_name     = "gpu_a100"
  key_pair        = var.key_pair
  security_groups = ["default"]

  network {
    name = var.network
  }
}

resource "openstack_compute_instance_v2" "gpu2" {
  name            = "transcept-gpu2"
  image_name      = "Ubuntu 22.04"
  flavor_name     = "gpu_a100"
  key_pair        = var.key_pair
  security_groups = ["default"]

  network {
    name = var.network
  }
}

resource "openstack_blockstorage_volume_v3" "persistent_volume" {
  name = "transcept-volume"
  size = 50
}
