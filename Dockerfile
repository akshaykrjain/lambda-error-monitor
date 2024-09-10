# Use Ubuntu as the base image
FROM ubuntu:latest

# Update the package list and install required dependencies
RUN apt-get update && \
    apt-get install -y curl unzip apt-transport-https ca-certificates gpg

# Download the public signing key for the Kubernetes package repositories
RUN curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.29/deb/Release.key | gpg --dearmor -o /usr/share/keyrings/kubernetes-archive-keyring.gpg

# Add the appropriate Kubernetes apt repository
RUN echo 'deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.29/deb/ /' > /etc/apt/sources.list.d/kubernetes.list

# Update apt package index
RUN apt-get update

# Install kubectl
RUN apt-get install -y kubectl

# Clean up unnecessary dependencies
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Test the installed version
RUN kubectl version --client


# Install Helm
RUN curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 && \
    chmod +x get_helm.sh && \
    ./get_helm.sh && \
    mv /usr/local/bin/helm /usr/bin/helm

# Clean up
RUN rm get_helm.sh

# Install Kustomize
RUN curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash && \
    chmod +x kustomize && \
    mv ./kustomize /usr/bin/kustomize

# Download and install awscli
RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ]; then \
    ARCH="x86_64"; \
    fi && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-${ARCH}.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install

# Cleanup
RUN rm awscliv2.zip && \
    rm -rf ./aws

RUN apt-get remove -y unzip apt-transport-https ca-certificates gpg

# Set PATH environment variable to include /usr/bin
ENV PATH="${PATH}:/usr/bin"

# Command to keep the container running (example: sleep infinity)
CMD ["sleep", "infinity"]
