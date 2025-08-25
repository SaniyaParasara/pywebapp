pipeline {
  agent any

  options {
    // Avoid double checkout noise: remove this if you prefer the default checkout stage
    skipDefaultCheckout(true)
  }

  stages {
    stage('Checkout') {
      steps {
        // Use job SCM or uncomment the explicit git line
        checkout scm
        // git branch: 'main', url: 'https://github.com/SaniyaParasara/pywebapp.git'
      }
    }

    stage('Build Image') {
      steps {
        sh '''
          set -e
          echo "Building Docker image..."
          docker build -t pywebapp:latest .
        '''
      }
    }

    stage('Test') {
      steps {
        sh '''
          set -e
          echo "Running pytest in container..."
          docker run --rm pywebapp:latest python -m pytest -q
        '''
      }
    }

    stage('Deploy') {
      steps {
        sh '''
          set -e
          echo "Deploying container on host port 3000 -> container 8000..."
          docker rm -f pyweb >/dev/null 2>&1 || true
          docker run -d --name pyweb -p 3000:8000 pywebapp:latest

          echo "Health check (inside pyweb's network namespace)..."
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
    failure { echo 'Pipeline failed. Check logs.' }
  }
}
