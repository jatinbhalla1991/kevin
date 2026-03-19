# Kubernetes Deployment Pipeline with Security Scanning

## Problem Statement

Your team has been tasked with setting up an automated deployment pipeline for a containerized application. The pipeline must build a Docker container, scan it for security vulnerabilities, and generate deployment-ready Kubernetes manifests.

## Current Situation

The infrastructure team has provided you with:
- A Python web application located at `/app/app.py`
- A Dockerfile template at `/app/Dockerfile`
- A Kubernetes deployment template at `/app/k8s-deployment.yaml`

However, the current setup is incomplete and not production-ready.

## Your Task

1. **Fix the Application**: The web application at `/app/app.py` has critical issues that prevent it from running properly in a containerized environment. Debug and fix these issues.

2. **Complete the Dockerfile**: The Dockerfile at `/app/Dockerfile` is incomplete. It needs proper configuration to:
   - Build successfully
   - Run the web application on port 8080
   - Follow Docker best practices for production

3. **Security Scanning**: Implement a security vulnerability scan of the Docker image. The scan results must be saved to `/app/security-report.json`. Critical vulnerabilities (if any) should be documented.

4. **Kubernetes Manifests**: Fix and validate the Kubernetes deployment manifest at `/app/k8s-deployment.yaml`. Ensure it:
   - References the correct container image
   - Exposes the service on the correct port
   - Includes proper health checks
   - Follows Kubernetes best practices

5. **Pipeline Script**: Create a deployment pipeline script at `/app/deploy.sh` that orchestrates all the steps:
   - Builds the Docker image
   - Runs security scanning
   - Validates the Kubernetes manifests
   - Outputs a deployment summary to `/app/deployment-summary.txt`

## Success Criteria

Your solution will be evaluated on:
- The application runs without errors
- The Docker image builds successfully
- Security scanning is performed and results are documented
- Kubernetes manifests are valid and production-ready
- All required output files are generated in the `/app/` directory

## Constraints

- The web application must listen on port 8080
- All output files must be created in the `/app/` directory
- Do not modify the test files or environment configuration
- The solution must be reproducible and automated

Good luck!