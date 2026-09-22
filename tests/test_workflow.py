import unittest
from src.workflow import choose_theme, run_quality_checks, process

class XWorkflowTests(unittest.TestCase):
    def test_failure_theme(self):
        self.assertEqual(
            choose_theme({"failure": "通知が二重送信された"}),
            "失敗から分かったこと"
        )

    def test_real_experience_check(self):
        checks = run_quality_checks({
            "experience": "Discord Botの定時通知が二重送信される問題を調査した",
            "failure": "",
            "discovery": ""
        })
        self.assertTrue(checks["has_real_experience"])
        self.assertTrue(checks["has_specific_fact"])

    def test_generic_content_requires_revision(self):
        result = process({
            "experience": "",
            "failure": "",
            "discovery": "",
            "goal": "交流",
            "external_publish": True
        })
        self.assertTrue(result.revision_required)
        self.assertEqual(result.status, "needs_revision")

    def test_external_publish_requires_human_review(self):
        result = process({
            "experience": "実際の改善作業で通知経路の重複を発見した",
            "failure": "最初の仮説が外れた",
            "discovery": "起動経路の確認が重要だった",
            "goal": "プロフィール訪問",
            "external_publish": True
        })
        self.assertTrue(result.human_review_required)
        self.assertEqual(result.status, "waiting_human_review")

if __name__ == "__main__":
    unittest.main()
