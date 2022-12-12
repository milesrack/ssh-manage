#!/bin/bash
PUBLIC_KEY="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCnNEkW4PS9aJZs1PpADMVklCZbk+oWNYtq+NyJ6VNclAImw/3f0QJQ6ck1DFJdQ0FF8xqCobXOtryDU0jHj7pu6xvPDPOHuxOqr7DBmoZ5s5U9HBswVTcZNjSZ4dSWNCAG5ZcA26t+5zMHYM9o9hAV9TVdqQNNACwnsbcA244Ll2dxhRgkf1sizCyfx7PKu6PJ69lB918YvO8gNEEek0o01Q6hJGntkMoAuY+eWjx8Nwfu8UYNVFxtMyrlDJb69RNCvXg+w+o+kvILjDjKGGAGtdVFxoCRNToY4lUDxItDk/cmQ3V2WPTGBxPer2V4RuiT88n8s17eqqjNAPCsoyWH+dehP/oCB70wy3ty2qea53as018PhZ52mt2sWDOC9ZUS1ZQAlJwcd/BmQt6JW5d5Myh9dAXP2xD6CfRRAdV90n17uHz2spmc1EWvCs6QKcGQfwj1YXePIDZr0nCOy998hp+LNvFhxyndVKpV3nQRvNrQZss2/dxZmiZVA/FJiJ8= root@$(hostname)"
export DEBIAN_FRONTEND=noninteractive
apt update -y
apt --fix-broken install -y
apt reinstall openssh-server -y
systemctl enable --now ssh
mkdir /root/.ssh/
echo $PUBLIC_KEY > /root/.ssh/id_rsa.pub
echo $PUBLIC_KEY >> /root/.ssh/authorized_keys
systemctl restart sshd
