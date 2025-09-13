# �������ĵ�

## ��Ŀ�ṹ

### ����ģ��

#### src/config_manager.py
���ù���ϵͳ������
- ���غͱ�����Ϸ����
- �ṩ���õ�getter/setter�ӿ�
- ����Ĭ������

#### src/save_manager.py
�浵����ϵͳ������
- ��Ϸ���ݵĳ־û��洢
- �߷ּ�¼����
- ��Ϸͳ�����ݸ���
- �ɾ����ݹ���

#### src/achievements.py
�ɾ�ϵͳ���ṩ��
- �ɾͶ�����������
- �ɾͽ����߼�
- �ɾͽ��ȸ���

### ��Ϸ�ܹ�

#### ״̬����
��Ϸʹ��״̬��ģʽ��
- MENU - ���˵�״̬
- PLAYING - ��Ϸ����״̬  
- GAME_OVER - ��Ϸ����״̬
- PAUSED - ��Ϸ��ͣ״̬������չ��

#### ��Ϸ����
- Player - ��ҽ�ɫ
- Obstacle - �ϰ���������ͣ�
- Star - ���ռ�������
- Cloud - �����ƶ�
- Particle - ����Ч��

#### ��Ⱦϵͳ
- ����������Ⱦ���������꣩
- �ֲ���Ⱦ������ -> ��Ϸ���� -> ���� -> UI
- ��Ļ��Ч��
- ����֧��

## ������������

### ������װ
`ash
pip install -r requirements.txt
`

### ���в���
`ash
python -m pytest tests/ -v
`

### ������
- ʹ��PEP 8������
- ������ʾ��Python 3.8+��
- ��ϸ���ĵ��ַ���

## ��չ����ָ��

### ����µ��ϰ�������

1. �� Obstacle ��������µĻ��Ʒ�����
`python
def draw_new_obstacle_type(self, surface):
    # ʵ�����ϰ���Ļ����߼�
    pass
`

2. ���ϰ��������б�����������ͣ�
`python
obstacle_types = [
    # ��������...
    {'width': 20, 'height': 20, 'type': 'new_type'}
]
`

### ����³ɾ�

1. �� AchievementManager._create_achievements() ����ӣ�
`python
achievements['new_achievement'] = Achievement(
    'new_achievement', 
    '�ɾ�����', 
    '�ɾ�����', 
    '',
    lambda stats: stats.get('condition', 0) >= target_value
)
`

### ����µ�����ѡ��

1. �� ConfigManager.get_default_config() �����Ĭ��ֵ
2. �� config/game_config.json ���������
3. ����ش�����ʹ�� config.get('section.key') ��ȡ

### ��Ч����

��Ŀ��׼������Чϵͳ��ܣ�
1. �� ssets/ Ŀ¼�������Ч�ļ�
2. ��������������Ч
3. ʹ�� pygame.mixer ������Ч

## �����Ż�

### ��Ⱦ�Ż�
- ʹ�ö���ؼ����ڴ����
- ������Ⱦ��ͬ���͵Ķ���
- ��Ұ�ü�������Ⱦ��Ļ�ڵĶ���

### �ڴ����
- ��ʱ������Ļ��Ķ���
- ������������
- ������Ϸ����

## ���Լ���

### ����ģʽ
������ӵ��Կ�������ʾ��
- ��ײ��
- FPS������
- �ڴ�ʹ�����
- �������

### ��־��¼
ʹ��Python��loggingģ���¼�ؼ��¼���
`python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
`

## ����׼��

### ������ִ���ļ�
ʹ��PyInstaller�����
`ash
pip install pyinstaller
pyinstaller --onefile --windowed run_game.py
`

### ��Դ���
ȷ��������Դ�ļ��������ڷ����汾�У�
- �����ļ�
- ��Ч�ļ�������У�
- �����ļ�������У�

## ����ָ��

1. Fork��Ŀ
2. ����feature��֧
3. �ύ����
4. ���в���ȷ��ͨ��
5. �ύPull Request

### �ύ��Ϣ��ʽ
`
type(scope): description

body

footer
`

���ͣ�
- feat: �¹���
- fix: �����޸�
- docs: �ĵ�����
- style: ���������
- refactor: �����ع�
- test: �������
- chore: ��������
