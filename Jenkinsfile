pipeline {
  agent any

  environment {
    // Compose project name so containers are predictable
    COMPOSE_PROJECT = "webapp"
    HEALTH_URL      = "http://localhost/healthz"
  }

  options {
    timestamps()
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Build & Up via Compose') {
      steps {
        sh """
          docker compose -p ${COMPOSE_PROJECT} down || true
          docker compose -p ${COMPOSE_PROJECT} up -d --build
        """
      }
    }

    stage('Smoke Test') {
      steps {
        sh """
          echo "Waiting for app..."
          for i in {1..20}; do
            if curl -fsS ${HEALTH_URL} | grep -q '"ok"'; then
              echo "Health OK"; exit 0
            fi
            sleep 2
          done
          echo "Health check failed"
          exit 1
        """
      }
    }
  }

  post {
    success {
      echo "✅ Deployed via Compose. Health OK."
      sh "docker compose -p ${COMPOSE_PROJECT} ps"
    }
    failure {
      echo "❌ Deployment failed. Recent web logs:"
      sh "docker logs webapp_live || true"
    }
  }
}
