variable "key_name" {
  description = "AWS key pair name"
  type        = string
}

variable "instance_type" {
  default     = "t3.micro"
}
