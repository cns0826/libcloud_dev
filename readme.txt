1. 수행 위치 
   개발 서버 접속 후 aliyun 디렉토리 이동

2. 입력 파일
   It's Box 작업 후 결과물인 Aliyun 관련 설정 파일이 저장된 xml 
   - 현재는 input.xml에 임시로 등록하여 사용함.
   - 추후, It's Box 개발 완료 시 연계 예정임.

2. 스크립트 실행 
   시작 : python aliyun_script_test_20161219_1.py input.xml 
   수행 시 주의 사항 :
          - 스크립트 후반 부에 신규 인스턴스 수 만큼 비밀 번호를 입력 필요함(인스턴스당 2번씩, ssh 1회, scp 1회)
          - 공개키를 신규 인스턴스 마다 등록하기 위함
          - 공개키 등록 후 saltstack minion 설치 및 yum update, /etc/hosts 파일에 saltstack master 등록은
            개인키로 접속 방식으로 자동 수행 됨.
	  - 공개키 : test_key_pair.pub 개인키 : test_key_pair

3. 결과 파일
   1. 스크립트 수행으로 생성된 Aliyun 환경 정보
      파일명 : 2016-12-19_08:15:45.txt 
      파일내용 : 
	EIP : 47.89.10.251
	EIP_ALLOCATION_ID : eip-j6cgvjyvof548pc2u5s98
	VSWITCH_ID : vsw-j6ccfr95e1z55qy4f0pvf
	Instance Size: ecs.n1.tiny
	Instance Image: centos7u2_64_40G_cloudinit_20160520.raw
	SecurityGroupId : sg-j6ca1eflc3vd6sqz5vv8
	NEW_VPC_ID : vpc-j6clckkbqd1dxx5iz01dk
	ZONE_ID : cn-hongkong-b
	PASSWORD : 1q2w3e4r!

   2. update_hosts.sh
      - 신규 인스턴스의 /etc/hosts에 saltstack 마스터 등록

   3. saltstack_install.sh
      - saltstack minion 설치 및 yum update 수행

   4. authorized_keys_update.sh
      - root 계정에 .ssh 디렉토리 생성, authorized_keys 파일 생성, 공개키 등록 


4. 환경 삭제
   - 수행 : python aliyun_delete.py 2016-12-19_08:15:45.txt
   - 스크립트 수행으로 생성된 ECS 인스턴스 , Vswitch, Security Group, EIP , VPC 모두 삭제
   - 결과파일 : 2016-12-19_08:15:45.txt_delete 


    
