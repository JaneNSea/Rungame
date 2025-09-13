#!/usr/bin/env python3
"""
��Ϸ�����ű�
��������ļ������� Pixel Runner Game
"""

import sys
import os

# ����srcĿ¼��Python·��
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

try:
    # ���Ե��벢������������Ϸ
    from src.game_v2 import main as game_v2_main
    print("���� Pixel Runner Game v2.0...")
    game_v2_main()
except ImportError:
    # ��������治���ã�����ԭ��
    print("�����治���ã�����ԭ����Ϸ...")
    try:
        import enhanced_game
        enhanced_game.main()
    except ImportError as e:
        print(f"�޷�������Ϸ: {e}")
        print("��ȷ����װ����������: pip install -r requirements.txt")
        sys.exit(1)
except Exception as e:
    print(f"��Ϸ����ʱ����: {e}")
    sys.exit(1)
