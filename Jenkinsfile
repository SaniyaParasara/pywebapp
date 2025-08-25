pipeline {
  agent any
  stages {
    stage('Checkout') { steps { checkout scm } } // keep if you use job SCM
    stage('Docker Build & Run') {
      environment {
        IMAGE = 'webapp:local'
        CNAME = 'webapp'
        APP_PORT = '8000' // match your Dockerfile/app port
      }
      steps {
        sh '''
          docker rm -f ${CNAME} || true
          docker build -t ${IMAGE} .
          docker run -d --name ${CNAME} -p ${APP_PORT}:${APP_PORT} ${IMAGE}
        '''
      }
    }
  }
  post {
    success { echo "Running at http://localhost:${APP_PORT}" }
  }
}
