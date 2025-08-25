pipeline {
  agent any

  // If your Jenkins runs in Docker on Windows and you exposed Docker Desktop on 2375, keep this.
  // Otherwise you can delete the environment block.
  environment {
    DOCKER_HOST = 'tcp://host.docker.internal:2375'
  }

  options {
    // Prevent the automatic "Declarative: Checkout SCM" to avoid double checkout logs
    skipDefaultCheckout(true)
  }

  stages {
    stage('Checkout') {
      steps {
        // EITHER use the job SCM:
        checkout scm
        // OR comment the above and use explicit git:
        // git branch: 'main', url: 'https://github.com/SaniyaParasara/pywebapp.git'
      }
    }

    stage('Build') {
      steps {
        sh '''
          set -e
          echo "Building the application (Docker image)..."
          docker build -t pywebapp:latest .
        '''
      }
    }

    stage('Test') {
      steps {
        sh '''
          set -e
          echo "Running tests (pytest) in container..."
          docker run --rm pywebapp:latest python -m pytest -q
        '''
      }
    }

    stage('Deploy') {
      steps {
        sh '''
          set -e
          echo "Deploying application..."
          # Map host 3000 -> container 8000 (Jenkins uses 8080, so 3000 avoids conflict)
          docker rm -f pyweb >/dev/null 2>&1 || true
          docker run -d --name pyweb -p 3000:8000 pywebapp:latest

          echo "Health check..."
          for i in $(seq 1 30); do
            if docker run --rm --network container:pyweb curlimages/curl:8.8.0 -fsS http://localhost:8000/healthz >/dev/null; then
              echo "App is healthy ✅"
              exit 0
            fi
            sleep 1
          done

          echo "Health check failed"
          docker logs pyweb || true
          exit 1
        '''
      }
    }
  }

  post {
    success { echo 'Pipeline completed successfully!' }
    failure { echo 'Pipeline failed. check logs.' }
  }
}
