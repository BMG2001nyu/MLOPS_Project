variable "auth_url" {
  description = "OpenStack auth URL"
  default     = "https://chi.tacc.chameleoncloud.org:5000/v3"
}

variable "tenant_name" {
  description = "Chameleon project name"
  default     = "CH-XXXXXX"
}

variable "user_name" {
  description = "Your Chameleon username"
}

variable "password" {
  description = "Your Chameleon password"
}

variable "region" {
  description = "Region to deploy in"
  default     = "RegionOne"
}

variable "domain_name" {
  description = "Default domain"
  default     = "Default"
}

variable "network" {
  description = "Network to attach instances to"
  default     = "sharednet1"
}

variable "key_pair" {
  description = "Your SSH key name in Chameleon"
  default     = "transcept-key"
}
