"""
社員管理システム - 統合版

全てのクラスと機能を1つのファイルにまとめたバージョンです。
このファイルを実行するだけでテストができます。
"""

from typing import List
from functools import wraps


# ============================================================
# Employeeクラス（基底クラス）
# ============================================================
class Employee:
    """
    社員の基底クラス
    
    すべての社員タイプの基本となるクラスです。
    名前と給料の情報を管理します。
    
    Attributes:
        _name (str): 社員の名前
        _salary (int): 社員の給料
    """
    
    def __init__(self):
        """Employeeクラスのコンストラクタ"""
        self._name: str = ""
        self._salary: int = 0
    
    def get_name(self) -> str:
        """
        社員の名前を取得する
        
        Returns:
            str: 社員の名前
        """
        return self._name
    
    def set_name(self, emp_name: str) -> None:
        """
        社員の名前を設定する
        
        Args:
            emp_name (str): 設定する社員の名前
        """
        self._name = emp_name
    
    def get_salary(self) -> int:
        """
        社員の給料を取得する
        
        Returns:
            int: 社員の給料
        """
        return self._salary
    
    def set_salary(self, emp_salary: int) -> None:
        """
        社員の給料を設定する
        
        Args:
            emp_salary (int): 設定する給料
        """
        self._salary = emp_salary
    
    def __del__(self):
        """デストラクタ - インスタンスが削除されるときに呼ばれる"""
        print(f"[デストラクタ] Employeeインスタンス '{self._name}' が削除されました")


# ============================================================
# Staffクラス（一般社員）
# ============================================================
class Staff(Employee):
    """
    一般社員クラス
    
    Employeeクラスを継承し、所属部署の情報を追加します。
    
    Attributes:
        _division (str): 所属部署
    """
    
    def __init__(self):
        """Staffクラスのコンストラクタ"""
        super().__init__()
        self._division: str = ""
    
    def get_division(self) -> str:
        """
        所属部署を取得する
        
        Returns:
            str: 所属部署名
        """
        return self._division
    
    def set_division(self, emp_division: str) -> None:
        """
        所属部署を設定する
        
        Args:
            emp_division (str): 設定する部署名
        """
        self._division = emp_division
    
    def __del__(self):
        """デストラクタ - インスタンスが削除されるときに呼ばれる"""
        print(f"[デストラクタ] Staffインスタンス '{self._name}' が削除されました")


# ============================================================
# Presidentクラス（社長）
# ============================================================
class President(Employee):
    """
    社長クラス
    
    Employeeクラスを継承し、会社への参照を持ちます。
    get_name()メソッドをオーバーライドして「社長」の肩書きを追加します。
    
    Attributes:
        _company (Company): 所属する会社のインスタンス
    """
    
    def __init__(self, company: 'Company'):
        """
        Presidentクラスのコンストラクタ
        
        Args:
            company (Company): 所属する会社のインスタンス
        """
        super().__init__()
        self._company: 'Company' = company
    
    def get_name(self) -> str:
        """
        社長の名前を取得する（オーバーライド）
        
        名前の末尾に「社長」の肩書きを追加します。
        
        Returns:
            str: 「社長」の肩書き付きの名前
        """
        return self._name + "社長"
    
    def dismiss(self, name: str) -> None:
        """
        指定された名前の社員を解雇する
        
        Args:
            name (str): 解雇する社員の名前
        """
        self._company._staffs = [
            staff for staff in self._company._staffs 
            if staff.get_name() != name
        ]
        print(f"[解雇通知] {name}さんを解雇しました")
    
    def __del__(self):
        """デストラクタ - インスタンスが削除されるときに呼ばれる"""
        print(f"[デストラクタ] Presidentインスタンス '{self._name}' が削除されました")


# ============================================================
# デコレータ関数
# ============================================================
def print_employee_count(func):
    """
    社員数を表示するデコレータ
    
    メソッド実行後に現在の社員数（社長含む）を表示します。
    
    Args:
        func: デコレートする関数
        
    Returns:
        ラップされた関数
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        total_employees = len(self._staffs) + 1  # スタッフ数 + 社長
        print(f"現在わが社の社員数は{total_employees}人になっています")
        return result
    return wrapper


# ============================================================
# Companyクラス（会社）
# ============================================================
class Company:
    """
    会社クラス
    
    社員（Staff）と社長（President）を管理します。
    
    Attributes:
        _staffs (List[Staff]): 社員のリスト
        _ceo (President): 社長
    """
    
    def __init__(self):
        """Companyクラスのコンストラクタ"""
        self._staffs: List[Staff] = []
        self._ceo: President = President(self)
    
    @property
    def staffs(self) -> List[Staff]:
        """
        社員リストを取得する（プロパティ）
        
        Returns:
            List[Staff]: 社員のリスト
        """
        return self._staffs
    
    @property
    def ceo(self) -> President:
        """
        社長を取得する（プロパティ）
        
        Returns:
            President: 社長のインスタンス
        """
        return self._ceo
    
    @print_employee_count
    def set_dismissal_procedure(self, name: str) -> None:
        """
        解雇手続きを実行する
        
        指定された名前の社員を解雇し、現在の社員数を表示します。
        このメソッドはデコレータにより社員数が自動表示されます。
        
        Args:
            name (str): 解雇する社員の名前
        """
        self._staffs = [
            staff for staff in self._staffs 
            if staff.get_name() != name
        ]
        print(f"[解雇手続き完了] {name}さんの解雇手続きが完了しました")
    
    def __del__(self):
        """デストラクタ - インスタンスが削除されるときに呼ばれる"""
        print("[デストラクタ] Companyインスタンスが削除されました")


# ============================================================
# メイン関数（テスト実行）
# ============================================================
def main():
    """
    メイン関数
    
    会社インスタンスを作成し、社員と社長を登録してテストします。
    """
    print("=" * 60)
    print("社員管理システム テスト開始")
    print("=" * 60)
    print()
    
    # 会社インスタンスの作成
    company = Company()
    
    # 社員1: 佐藤太郎
    staff1 = Staff()
    staff1.set_name("佐藤太郎")
    staff1.set_salary(200000)
    staff1.set_division("営業部")
    company.staffs.append(staff1)
    
    # 社員2: 鈴木次郎
    staff2 = Staff()
    staff2.set_name("鈴木次郎")
    staff2.set_salary(300000)
    staff2.set_division("開発部")
    company.staffs.append(staff2)
    
    # 社長: 偉井杉人
    company.ceo.set_name("偉井杉人")
    company.ceo.set_salary(2500000)
    
    # 社員情報の出力
    print("【社員一覧】")
    for staff in company.staffs:
        print(f"名前：{staff.get_name()}、給料：{staff.get_salary()}円、所属：{staff.get_division()}")
    
    print()
    print("【社長情報】")
    print(f"名前：{company.ceo.get_name()}、給料：{company.ceo.get_salary()}円")
    
    print()
    print("=" * 60)
    print("追加機能テスト")
    print("=" * 60)
    print()
    
    # dismissメソッドのテスト
    print("【社長によるdismissメソッドテスト】")
    print(f"解雇前の社員数: {len(company.staffs)}人")
    company.ceo.dismiss("佐藤太郎")
    print(f"解雇後の社員数: {len(company.staffs)}人")
    print()
    
    # 佐藤太郎を再追加（次のテストのため）
    staff3 = Staff()
    staff3.set_name("佐藤太郎")
    staff3.set_salary(200000)
    staff3.set_division("営業部")
    company.staffs.append(staff3)
    print(f"佐藤太郎を再雇用しました（現在の社員数: {len(company.staffs)}人）")
    print()
    
    # set_dismissal_procedureメソッドのテスト（デコレータ付き）
    print("【デコレータ付きset_dismissal_procedureメソッドテスト】")
    company.set_dismissal_procedure("鈴木次郎")
    print()
    
    # 残っている社員の確認
    print("【最終的な社員一覧】")
    for staff in company.staffs:
        print(f"名前：{staff.get_name()}、給料：{staff.get_salary()}円、所属：{staff.get_division()}")
    print()
    print(f"社長：{company.ceo.get_name()}")
    
    print()
    print("=" * 60)
    print("デストラクタのテスト（プログラム終了時に表示されます）")
    print("=" * 60)


# ============================================================
# プログラムのエントリーポイント
# ============================================================
if __name__ == "__main__":
    main()
    print("\n[プログラム終了 - デストラクタが呼ばれます]")

# employee_system_all_in_one.py
