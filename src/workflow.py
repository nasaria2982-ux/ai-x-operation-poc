from dataclasses import dataclass, asdict

@dataclass
class XWorkflowResult:
    theme: str
    goal: str
    post_structure: list[str]
    quality_checks: dict
    revision_required: bool
    human_review_required: bool
    status: str

    def to_dict(self):
        return asdict(self)

def choose_theme(data):
    if data.get("failure"):
        return "失敗から分かったこと"
    if data.get("discovery"):
        return "実践して分かったこと"
    return "最近の実体験からの気づき"

def build_structure(data):
    structure = ["意外な結論", "実際に起きた出来事"]
    if data.get("failure"):
        structure.append("失敗・想定外")
    if data.get("discovery"):
        structure.append("学び")
    structure.append("読者への示唆")
    return structure

def run_quality_checks(data):
    experience = data.get("experience", "").strip()
    failure = data.get("failure", "").strip()
    discovery = data.get("discovery", "").strip()

    has_real_experience = bool(experience)
    has_specific_fact = len(experience) >= 12 or bool(failure)
    too_generic = not (experience or failure or discovery)

    return {
        "has_real_experience": has_real_experience,
        "has_specific_fact": has_specific_fact,
        "too_generic": too_generic,
    }

def process(data):
    checks = run_quality_checks(data)
    revision_required = (
        not checks["has_real_experience"]
        or not checks["has_specific_fact"]
        or checks["too_generic"]
    )
    human_review = bool(data.get("external_publish", True))

    return XWorkflowResult(
        theme=choose_theme(data),
        goal=data.get("goal", "交流"),
        post_structure=build_structure(data),
        quality_checks=checks,
        revision_required=revision_required,
        human_review_required=human_review,
        status="needs_revision" if revision_required else (
            "waiting_human_review" if human_review else "ready"
        ),
    )
