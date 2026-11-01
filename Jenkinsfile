pipeline {
    agent {
        label 'linux'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Source code checkout'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies'
                sh '''
                    python3 -m venv venv
                    venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running application tests'
                sh 'venv/bin/python -m pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image'
                sh 'docker build -t devops-cicd-app:latest .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_TOKEN'
                )]) {
                    sh '''
                        set +x
                        echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USER" --password-stdin
                        trap 'docker logout >/dev/null 2>&1 || true' EXIT

                        docker tag devops-cicd-app:latest "$DOCKERHUB_USER/devops-cicd-app:${BUILD_NUMBER}"
                        docker tag devops-cicd-app:latest "$DOCKERHUB_USER/devops-cicd-app:latest"

                        docker push "$DOCKERHUB_USER/devops-cicd-app:${BUILD_NUMBER}"
                        docker push "$DOCKERHUB_USER/devops-cicd-app:latest"
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'CI Pipeline completed successfully!'
        }
        failure {
            echo 'CI Pipeline failed. Check the console output.'
        }
    }
}