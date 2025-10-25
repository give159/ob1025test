"""
社員管理システム - インポート版テストケースファイル

メインファイル（employee_system_all_in_one.py）から
クラスをインポートしてテストします。
"""

import unittest
import sys
from io import StringIO

# メインファイルからクラスをインポート
# ファイル名から .py を除いた名前を指定
from employee_system_all_in_one import (
    Employee,
    Staff, 
    President,
    Company
)


# ============================================================
# テストケース
# ============================================================

class TestEmployee(unittest.TestCase):
    """Employeeクラスのテストケース"""
    
    def setUp(self):
        """各テストの前に実行される準備処理"""
        self.employee = Employee()
    
    def test_initial_values(self):
        """初期値のテスト"""
        self.assertEqual(self.employee.get_name(), "")
        self.assertEqual(self.employee.get_salary(), 0)
        print("✓ Employeeの初期値テスト成功")
    
    def test_set_and_get_name(self):
        """名前の設定と取得のテスト"""
        self.employee.set_name("山田太郎")
        self.assertEqual(self.employee.get_name(), "山田太郎")
        print("✓ 名前の設定・取得テスト成功")
    
    def test_set_and_get_salary(self):
        """給料の設定と取得のテスト"""
        self.employee.set_salary(300000)
        self.assertEqual(self.employee.get_salary(), 300000)
        print("✓ 給料の設定・取得テスト成功")
    
    def test_name_update(self):
        """名前の更新テスト"""
        self.employee.set_name("田中一郎")
        self.assertEqual(self.employee.get_name(), "田中一郎")
        self.employee.set_name("田中次郎")
        self.assertEqual(self.employee.get_name(), "田中次郎")
        print("✓ 名前の更新テスト成功")


class TestStaff(unittest.TestCase):
    """Staffクラスのテストケース"""
    
    def setUp(self):
        """各テストの前に実行される準備処理"""
        self.staff = Staff()
    
    def test_inheritance(self):
        """継承のテスト"""
        self.assertIsInstance(self.staff, Employee)
        self.assertTrue(hasattr(self.staff, 'get_name'))
        self.assertTrue(hasattr(self.staff, 'get_salary'))
        print("✓ Staff継承テスト成功")
    
    def test_division_initial_value(self):
        """部署の初期値テスト"""
        self.assertEqual(self.staff.get_division(), "")
        print("✓ 部署の初期値テスト成功")
    
    def test_set_and_get_division(self):
        """部署の設定と取得のテスト"""
        self.staff.set_division("開発部")
        self.assertEqual(self.staff.get_division(), "開発部")
        print("✓ 部署の設定・取得テスト成功")
    
    def test_complete_staff_data(self):
        """完全な社員データのテスト"""
        self.staff.set_name("佐藤太郎")
        self.staff.set_salary(200000)
        self.staff.set_division("営業部")
        
        self.assertEqual(self.staff.get_name(), "佐藤太郎")
        self.assertEqual(self.staff.get_salary(), 200000)
        self.assertEqual(self.staff.get_division(), "営業部")
        print("✓ 完全な社員データテスト成功")


class TestPresident(unittest.TestCase):
    """Presidentクラスのテストケース"""
    
    def setUp(self):
        """各テストの前に実行される準備処理"""
        self.company = Company()
        self.president = self.company.ceo
    
    def test_inheritance(self):
        """継承のテスト"""
        self.assertIsInstance(self.president, Employee)
        print("✓ President継承テスト成功")
    
    def test_name_override(self):
        """get_name()のオーバーライドテスト"""
        self.president.set_name("偉井杉人")
        self.assertEqual(self.president.get_name(), "偉井杉人社長")
        print("✓ 名前オーバーライドテスト成功")
    
    def test_company_reference(self):
        """会社インスタンスへの参照テスト"""
        self.assertIsNotNone(self.president._company)
        self.assertEqual(self.president._company, self.company)
        print("✓ 会社参照テスト成功")
    
    def test_dismiss_method(self):
        """dismissメソッドのテスト"""
        # 社員を追加
        staff1 = Staff()
        staff1.set_name("山田太郎")
        self.company.staffs.append(staff1)
        
        staff2 = Staff()
        staff2.set_name("田中花子")
        self.company.staffs.append(staff2)
        
        # 解雇前の確認
        self.assertEqual(len(self.company.staffs), 2)
        
        # 解雇実行
        self.president.dismiss("山田太郎")
        
        # 解雇後の確認
        self.assertEqual(len(self.company.staffs), 1)
        self.assertEqual(self.company.staffs[0].get_name(), "田中花子")
        print("✓ dismissメソッドテスト成功")


class TestCompany(unittest.TestCase):
    """Companyクラスのテストケース"""
    
    def setUp(self):
        """各テストの前に実行される準備処理"""
        self.company = Company()
    
    def test_initial_state(self):
        """初期状態のテスト"""
        self.assertEqual(len(self.company.staffs), 0)
        self.assertIsNotNone(self.company.ceo)
        print("✓ 初期状態テスト成功")
    
    def test_staffs_property(self):
        """staffsプロパティのテスト"""
        self.assertIsInstance(self.company.staffs, list)
        print("✓ staffsプロパティテスト成功")
    
    def test_ceo_property(self):
        """ceoプロパティのテスト"""
        self.assertIsInstance(self.company.ceo, President)
        print("✓ ceoプロパティテスト成功")
    
    def test_add_staff(self):
        """社員追加のテスト"""
        staff = Staff()
        staff.set_name("鈴木次郎")
        self.company.staffs.append(staff)
        
        self.assertEqual(len(self.company.staffs), 1)
        self.assertEqual(self.company.staffs[0].get_name(), "鈴木次郎")
        print("✓ 社員追加テスト成功")
    
    def test_multiple_staff(self):
        """複数社員の管理テスト"""
        for i in range(5):
            staff = Staff()
            staff.set_name(f"社員{i+1}")
            staff.set_salary(200000 + i * 10000)
            staff.set_division(f"部署{i+1}")
            self.company.staffs.append(staff)
        
        self.assertEqual(len(self.company.staffs), 5)
        print("✓ 複数社員管理テスト成功")
    
    def test_set_dismissal_procedure(self):
        """解雇手続きメソッドのテスト"""
        # 社員を追加
        staff1 = Staff()
        staff1.set_name("佐藤太郎")
        self.company.staffs.append(staff1)
        
        staff2 = Staff()
        staff2.set_name("鈴木次郎")
        self.company.staffs.append(staff2)
        
        # 解雇前の確認
        self.assertEqual(len(self.company.staffs), 2)
        
        # 標準出力をキャプチャ（デコレータの出力を抑制）
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # 解雇実行
        self.company.set_dismissal_procedure("佐藤太郎")
        
        # 標準出力を復元
        sys.stdout = sys.__stdout__
        
        # 解雇後の確認
        self.assertEqual(len(self.company.staffs), 1)
        self.assertEqual(self.company.staffs[0].get_name(), "鈴木次郎")
        print("✓ 解雇手続きテスト成功")


class TestIntegration(unittest.TestCase):
    """統合テスト - 実際のシナリオをテスト"""
    
    def test_complete_scenario(self):
        """完全なシナリオテスト"""
        print("\n" + "="*60)
        print("統合テスト: 完全なシナリオ実行")
        print("="*60)
        
        # 会社作成
        company = Company()
        print("1. 会社インスタンス作成 ✓")
        
        # 社員追加
        staff1 = Staff()
        staff1.set_name("佐藤太郎")
        staff1.set_salary(200000)
        staff1.set_division("営業部")
        company.staffs.append(staff1)
        print(f"2. {staff1.get_name()}を追加 ✓")
        
        staff2 = Staff()
        staff2.set_name("鈴木次郎")
        staff2.set_salary(300000)
        staff2.set_division("開発部")
        company.staffs.append(staff2)
        print(f"3. {staff2.get_name()}を追加 ✓")
        
        # 社長設定
        company.ceo.set_name("偉井杉人")
        company.ceo.set_salary(2500000)
        print(f"4. {company.ceo.get_name()}を設定 ✓")
        
        # 検証
        self.assertEqual(len(company.staffs), 2)
        self.assertEqual(company.ceo.get_name(), "偉井杉人社長")
        print("5. 社員数と社長名を検証 ✓")
        
        # 社員情報表示
        print("\n現在の社員:")
        for staff in company.staffs:
            print(f"  - {staff.get_name()}: {staff.get_salary()}円, {staff.get_division()}")
        print(f"社長: {company.ceo.get_name()}: {company.ceo.get_salary()}円")
        
        # 解雇
        print(f"\n6. {staff1.get_name()}を解雇")
        company.ceo.dismiss("佐藤太郎")
        self.assertEqual(len(company.staffs), 1)
        print("   解雇完了 ✓")
        
        # 最終確認
        remaining_staff = company.staffs[0]
        self.assertEqual(remaining_staff.get_name(), "鈴木次郎")
        self.assertEqual(remaining_staff.get_salary(), 300000)
        self.assertEqual(remaining_staff.get_division(), "開発部")
        
        print("\n最終社員:")
        print(f"  - {remaining_staff.get_name()}: {remaining_staff.get_salary()}円, {remaining_staff.get_division()}")
        print("="*60)
        print("統合テスト完了 ✓✓✓")
        print("="*60)


# ============================================================
# テスト実行部分
# ============================================================

def run_tests_with_summary():
    """テストを実行してサマリーを表示"""
    print("\n" + "="*60)
    print("社員管理システム テスト実行")
    print("="*60)
    print(f"インポート元: employee_system_all_in_one.py")
    print("="*60 + "\n")
    
    # テストスイートの作成
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 各テストクラスを追加
    suite.addTests(loader.loadTestsFromTestCase(TestEmployee))
    suite.addTests(loader.loadTestsFromTestCase(TestStaff))
    suite.addTests(loader.loadTestsFromTestCase(TestPresident))
    suite.addTests(loader.loadTestsFromTestCase(TestCompany))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # テスト実行
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 結果サマリー
    print("\n" + "="*60)
    print("テスト結果サマリー")
    print("="*60)
    print(f"実行テスト数: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失敗: {len(result.failures)}")
    print(f"エラー: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n🎉 すべてのテストが成功しました！")
    else:
        print("\n❌ いくつかのテストが失敗しました")
    
    print("="*60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    try:
        success = run_tests_with_summary()
        sys.exit(0 if success else 1)
    except ImportError as e:
        print("="*60)
        print("❌ インポートエラー")
        print("="*60)
        print(f"エラー内容: {e}")
        print("\n解決方法:")
        print("1. employee_system_all_in_one.py が同じフォルダにあるか確認")
        print("2. ファイル名が正しいか確認")
        print("3. 以下のコマンドでファイルを確認:")
        print("   dir *.py")
        print("="*60)
        sys.exit(1)
        
#test_import_main.py 
