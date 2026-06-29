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
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    . venv/bin/activate
                    pylint app.py --exit-zero
                '''
            }
        }

        stage('Security Scan') {
            steps {
                sh '''
                    . venv/bin/activate
                    bandit -r app.py -l
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
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
                sh '''
                    . venv/bin/activate
                    pkill -f "python3 app.py" || true
                    nohup python3 app.py --host=0.0.0.0 --port=5000 > flask.log 2>&1 &
                    echo "Deployed on port 5000"
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
