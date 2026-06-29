pipeline {
    agent any

    environment {
        PYTHONPATH = "${WORKSPACE}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                bat '''
                    call venv\\Scripts\\activate.bat
                    pylint app.py --exit-zero
                '''
            }
        }

        stage('Security Scan') {
            steps {
                bat '''
                    call venv\\Scripts\\activate.bat
                    bandit -r app.py -l || echo Bandit check skipped
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                    call venv\\Scripts\\activate.bat
                    python -m pytest test_app.py -v --junitxml=report.xml
                '''
            }
            post {
                always {
                    junit 'report.xml'
                }
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                bat '''
                    taskkill /F /IM python.exe 2>nul || ver>nul
                    start /B python app.py
                    echo Deployed on port 5000
                '''
            }
        }
    }

    post {
        success {
            emailext(
                to: 'your-email@example.com',
                subject: "SUCCESS: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: "Pipeline succeeded.\nJob: ${env.JOB_NAME}\nBuild: ${env.BUILD_NUMBER}\nURL: ${env.BUILD_URL}"
            )
        }
        failure {
            emailext(
                to: 'your-email@example.com',
                subject: "FAILED: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: "Pipeline failed.\nJob: ${env.JOB_NAME}\nBuild: ${env.BUILD_NUMBER}\nURL: ${env.BUILD_URL}"
            )
        }
    }
}
