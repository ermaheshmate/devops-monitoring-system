pipeline {
    agent any

    stages {
        stage('Deploy to EC2') {
            steps {
                sshagent(credentials: ['ec2-ssh-key']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no ec2-user@13.203.220.202 "
                            cd ~/devops-monitoring-system &&
                            git pull origin main &&
                            docker compose down &&
                            docker compose up -d --build
                        "
                    '''
                }
            }
        }
    }
}
