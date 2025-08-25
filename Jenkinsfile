pipeline {
  agent any

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
        echo 'Building the application...'
        // sh 'docker build -t webapp:latest .'
      }
    }

    stage('Test') {
      steps {
        echo 'Running tests...'
        // sh 'docker run --rm webapp:latest npm test'
      }
    }

    stage('Deploy') {
      steps {
        echo 'Deploying application...'
        // sh 'docker run -d -p 3000:3000 --name webapp webapp:latest'
      }
    }
  }

  post {
    success { echo 'Pipeline completed successfully!' }
    failure { echo 'Pipeline failed. check logs.' }
  }
}
