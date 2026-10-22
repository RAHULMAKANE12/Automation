
pipeline {
    agent any

    stages {
        stage('Checkout GitHub') {
            steps {
                checkout scm
            }
        }

        stage('Check Docker') {
            steps {
                bat 'docker --version'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t hackforge-registration .'
            }
        }

        
stage('Start Test Environment') {
    steps {
        bat '''
            docker rm -f hackforge-test-app hackforge-selenium 2>NUL
            docker run -d --name hackforge-test-app -p 5001:5000 hackforge-registration
            docker run -d --name hackforge-selenium -p 4444:4444 selenium/standalone-chrome:latest
            powershell -NoProfile -Command "Start-Sleep -Seconds 20"
        '''
    }
}


        stage('Run Selenium Tests') {
            steps {
                bat '''
                    docker run --rm ^
                    -v "%CD%:/workspace" ^
                    -w /workspace ^
                    -e SELENIUM_URL=http://host.docker.internal:4444/wd/hub ^
                    -e APP_URL=http://host.docker.internal:5001 ^
                    python:3.13-slim ^
                    sh -c "pip install --no-cache-dir selenium && python 'New folder/test_selenium.py'"
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                bat '''
                    docker rm -f hackforge-app 2>NUL
                    docker run -d --name hackforge-app -p 5000:5000 hackforge-registration
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                bat 'docker ps --filter "name=hackforge-app"'
            }
        }
    }

    post {
        always {
            bat '''
                docker rm -f hackforge-test-app hackforge-selenium 2>NUL
                exit /b 0
            '''
        }
    }
}
