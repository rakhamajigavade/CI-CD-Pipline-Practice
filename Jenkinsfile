
pipeline {
    agent {
        label 'linux'
    }

    environment {
        EC2_HOST = '13.53.38.195'
        EC2_USER = 'ubuntu'
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

        stage('Deploy to EC2') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    ),
                    sshUserPrivateKey(
                        credentialsId: 'ec2-ssh-key',
                        keyFileVariable: 'EC2_KEY'
                    )
                ]) {
                    sh '''
                        set -e

                        DOCKER_IMAGE="$DOCKERHUB_USER/devops-cicd-app:${BUILD_NUMBER}"

                        ssh -o StrictHostKeyChecking=no \
                            -i "$EC2_KEY" \
                            "$EC2_USER@$EC2_HOST" \
                            "DOCKER_IMAGE='$DOCKER_IMAGE' bash -s" <<'REMOTE'

                        set -e

                        echo "Pulling latest application image..."
                        docker pull "$DOCKER_IMAGE"

                        echo "Removing previous project container..."
                        docker rm -f devops-cicd-app || true

                        echo "Starting new application container..."
                        docker run -d \
                            --name devops-cicd-app \
                            --restart unless-stopped \
                            -p 80:5000 \
                            "$DOCKER_IMAGE"

                        echo "Checking application health..."

                        for i in $(seq 1 10); do
                            if curl -fsS http://localhost/health; then
                                echo "Deployment successful!"
                                exit 0
                            fi
                            sleep 3
                        done

                        echo "Health check failed!"
                        exit 1

                        REMOTE
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'CI/CD Pipeline completed successfully!'
        }

        failure {
            echo 'CI/CD Pipeline failed. Check the console output.'
        }
    }
}
