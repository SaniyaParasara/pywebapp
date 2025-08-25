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

    stage('Build Image') {
      steps {
        powershell '''
          Write-Host "Building Docker image..."
          docker build -t pywebapp:latest .
        '''
      }
    }

    stage('Test') {
      steps {
        powershell '''
          Write-Host "Running pytest in container..."
          docker run --rm pywebapp:latest python -m pytest -q
        '''
      }
    }

    stage('Deploy') {
      steps {
        powershell '''
          Write-Host "Deploying container..."
          docker rm -f pyweb 2>$null
          docker run -d -p 8000:8000 --name pyweb pywebapp:latest

          # Health check loop (up to ~30s)
          $ok = $false
          for ($i=1; $i -le 30; $i++) {
            try {
              $r = Invoke-WebRequest -UseBasicParsing -Uri http://localhost:8000/healthz -TimeoutSec 2
              if ($r.StatusCode -eq 200) { $ok = $true; break }
            } catch { Start-Sleep -Milliseconds 1000 }
          }
          if (-not $ok) { Write-Host "Health check failed"; exit 1 }
          Write-Host "App is healthy ✅"
        '''
      }
    }
  }

  post {
    success { powershell 'Write-Host "Pipeline completed successfully!"' }
    failure { powershell 'Write-Host "Pipeline failed. Check logs."' }
  }
}
