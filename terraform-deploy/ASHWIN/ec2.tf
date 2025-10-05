resource "aws_instance" "usp_ec2" {
  ami           = "ami-0dee22c13ea7a9a67"   
  instance_type = var.instance_type
  key_name      = var.key_name
  user_data = <<-EOF
              #!/bin/bash
              # Update packages
              apt-get update -y
              apt-get install -y docker.io

              # Enable and start Docker
              systemctl enable docker
              systemctl start docker

              # Pull your Docker image from Docker Hub
              docker pull ashwin2635/usp-app:v1

              # Run the container, exposing port 5000
              docker run -d -p 5000:5000 ashwin2635/usp-app:v1
              EOF
  tags = {
    Name = "USP"
  }
}
