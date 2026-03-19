"""
Use this file to define pytest tests that verify the outputs of the task.

This file will be copied to /tests/test_outputs.py and run by the /tests/test.sh file
from the working directory.
"""
import os
import json
import yaml
import re


def test_app_py_exists():
    """Test that app.py exists."""
    assert os.path.exists('/app/app.py'), "app.py file not found"


def test_app_py_has_correct_port():
    """Test that app.py is configured to run on port 8080."""
    with open('/app/app.py', 'r') as f:
        content = f.read()
    
    # Should use port 8080 or environment variable with 8080 as default
    assert '8080' in content, "app.py should use port 8080"
    

def test_app_py_has_correct_host():
    """Test that app.py is configured with proper host for containers."""
    with open('/app/app.py', 'r') as f:
        content = f.read()
    
    # Should bind to 0.0.0.0 to accept connections from outside the container
    assert '0.0.0.0' in content, "app.py should bind to host 0.0.0.0"


def test_app_py_not_debug_mode():
    """Test that app.py is not running in debug mode for production."""
    with open('/app/app.py', 'r') as f:
        content = f.read()
    
    # Should have debug=False or not specify debug at all in production
    assert 'debug=False' in content or ('app.run' in content and 'debug=True' not in content), \
        "app.py should not run in debug mode"


def test_dockerfile_exists():
    """Test that Dockerfile exists."""
    assert os.path.exists('/app/Dockerfile'), "Dockerfile not found"


def test_dockerfile_installs_requirements():
    """Test that Dockerfile installs Python requirements."""
    with open('/app/Dockerfile', 'r') as f:
        content = f.read()
    
    # Should have pip install command for requirements
    assert 'pip install' in content and 'requirements.txt' in content, \
        "Dockerfile should install requirements from requirements.txt"


def test_dockerfile_exposes_port():
    """Test that Dockerfile exposes port 8080."""
    with open('/app/Dockerfile', 'r') as f:
        content = f.read()
    
    assert 'EXPOSE 8080' in content, "Dockerfile should expose port 8080"


def test_dockerfile_has_cmd():
    """Test that Dockerfile has a CMD to run the application."""
    with open('/app/Dockerfile', 'r') as f:
        content = f.read()
    
    # Should have CMD or ENTRYPOINT to run the app
    assert 'CMD' in content or 'ENTRYPOINT' in content, \
        "Dockerfile should have CMD or ENTRYPOINT to run the application"


def test_k8s_deployment_exists():
    """Test that Kubernetes deployment manifest exists."""
    assert os.path.exists('/app/k8s-deployment.yaml'), "k8s-deployment.yaml not found"


def test_k8s_deployment_valid_yaml():
    """Test that k8s-deployment.yaml is valid YAML."""
    with open('/app/k8s-deployment.yaml', 'r') as f:
        data = yaml.safe_load_all(f)
        docs = list(data)
    
    assert len(docs) > 0, "k8s-deployment.yaml should contain at least one YAML document"


def test_k8s_deployment_has_correct_port():
    """Test that Kubernetes deployment uses port 8080."""
    with open('/app/k8s-deployment.yaml', 'r') as f:
        docs = list(yaml.safe_load_all(f))
    
    # Find deployment
    deployment = None
    for doc in docs:
        if doc and doc.get('kind') == 'Deployment':
            deployment = doc
            break
    
    assert deployment is not None, "Deployment resource not found in k8s-deployment.yaml"
    
    # Check container port
    containers = deployment['spec']['template']['spec']['containers']
    assert len(containers) > 0, "No containers defined in deployment"
    
    container_port = containers[0]['ports'][0]['containerPort']
    assert container_port == 8080, f"Container port should be 8080, got {container_port}"


def test_k8s_deployment_has_health_checks():
    """Test that Kubernetes deployment has health checks."""
    with open('/app/k8s-deployment.yaml', 'r') as f:
        docs = list(yaml.safe_load_all(f))
    
    deployment = None
    for doc in docs:
        if doc and doc.get('kind') == 'Deployment':
            deployment = doc
            break
    
    assert deployment is not None, "Deployment resource not found"
    
    container = deployment['spec']['template']['spec']['containers'][0]
    
    assert 'livenessProbe' in container, "Deployment should have livenessProbe"
    assert 'readinessProbe' in container, "Deployment should have readinessProbe"


def test_k8s_deployment_has_resource_limits():
    """Test that Kubernetes deployment has resource limits."""
    with open('/app/k8s-deployment.yaml', 'r') as f:
        docs = list(yaml.safe_load_all(f))
    
    deployment = None
    for doc in docs:
        if doc and doc.get('kind') == 'Deployment':
            deployment = doc
            break
    
    assert deployment is not None, "Deployment resource not found"
    
    container = deployment['spec']['template']['spec']['containers'][0]
    
    assert 'resources' in container, "Deployment should have resource limits"
    assert 'limits' in container['resources'], "Deployment should have resource limits"
    assert 'requests' in container['resources'], "Deployment should have resource requests"


def test_k8s_service_has_correct_target_port():
    """Test that Kubernetes service targets port 8080."""
    with open('/app/k8s-deployment.yaml', 'r') as f:
        docs = list(yaml.safe_load_all(f))
    
    service = None
    for doc in docs:
        if doc and doc.get('kind') == 'Service':
            service = doc
            break
    
    assert service is not None, "Service resource not found in k8s-deployment.yaml"
    
    target_port = service['spec']['ports'][0]['targetPort']
    assert target_port == 8080, f"Service targetPort should be 8080, got {target_port}"


def test_deploy_script_exists():
    """Test that deploy.sh script was created."""
    assert os.path.exists('/app/deploy.sh'), "deploy.sh script not found"


def test_deploy_script_is_executable():
    """Test that deploy.sh is executable."""
    import stat
    st = os.stat('/app/deploy.sh')
    is_executable = bool(st.st_mode & stat.S_IXUSR)
    assert is_executable, "deploy.sh should be executable"


def test_security_report_exists():
    """Test that security report was generated."""
    assert os.path.exists('/app/security-report.json'), \
        "security-report.json not found - pipeline should generate security scan results"


def test_security_report_valid_json():
    """Test that security report is valid JSON."""
    with open('/app/security-report.json', 'r') as f:
        data = json.load(f)
    
    assert isinstance(data, dict), "security-report.json should contain a JSON object"


def test_security_report_has_required_fields():
    """Test that security report contains required fields."""
    with open('/app/security-report.json', 'r') as f:
        data = json.load(f)
    
    assert 'summary' in data or 'vulnerabilities' in data, \
        "security-report.json should contain vulnerability information"


def test_deployment_summary_exists():
    """Test that deployment summary was generated."""
    assert os.path.exists('/app/deployment-summary.txt'), \
        "deployment-summary.txt not found - pipeline should generate deployment summary"


def test_deployment_summary_not_empty():
    """Test that deployment summary is not empty."""
    with open('/app/deployment-summary.txt', 'r') as f:
        content = f.read()
    
    assert len(content) > 0, "deployment-summary.txt should not be empty"


def test_deployment_summary_contains_status():
    """Test that deployment summary contains status information."""
    with open('/app/deployment-summary.txt', 'r') as f:
        content = f.read()
    
    # Should contain some indication of success/failure and component status
    assert 'success' in content.lower() or 'status' in content.lower(), \
        "deployment-summary.txt should contain status information"


def test_requirements_txt_exists():
    """Test that requirements.txt exists."""
    assert os.path.exists('/app/requirements.txt'), "requirements.txt not found"


def test_requirements_has_flask():
    """Test that Flask is in requirements."""
    with open('/app/requirements.txt', 'r') as f:
        content = f.read().lower()
    
    assert 'flask' in content, "requirements.txt should include Flask"

