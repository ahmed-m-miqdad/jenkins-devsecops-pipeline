pipeline {
    agent any 

    environment {
        APP_NAME       = "my-flask-app"
        IMAGE_NAME     = "local-app/${APP_NAME}:latest"
        PORT           = "5000"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Pulling latest code from GitHub...'
                checkout scm
            }
        }

        stage('Unit Tests') {              
            steps {
                echo 'Running automated Pytest suite...'
                dir('app') {
                    sh """
                        docker build -t test-runner .
                        docker run --rm test-runner sh -c "pip install pytest && pytest test_app.py -v"
                    """
                }
            }
        }

        stage('Security Scan') {           
            steps {
                echo 'Running Bandit Security Scan on Python code...'
                sh "docker run --rm test-runner bandit -r . -v || true"
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building production Docker image: ${IMAGE_NAME}..."
                dir('app') {
                    sh "docker build -t ${IMAGE_NAME} ."
                }
            }
        }

        stage('Approval Gate') {
            steps {
                input message: "Do you want to deploy ${APP_NAME} to production server?", ok: "Approve & Deploy"
            }
        }

        stage('Deploy to Prod') {
            steps {
                echo "Deploying application container..."
                sh """
                    docker rm -f ${APP_NAME} || true
                    docker run -d --name ${APP_NAME} -p ${PORT}:5000 ${IMAGE_NAME}
                """
                echo "Deployment successful! App is live."
            }
        }
    }

    
    post {
        always {
            echo 'Cleaning up intermediate build layers...'
            sh "docker image prune -f || true"
        }
        success {
            echo "SUCCESS: Pipeline completed flawlessly. Application deployed successfully."
        }
        failure {
            echo "FAILURE: Pipeline failed at some stage. Please investigate the logs immediately."
        }
    }
}