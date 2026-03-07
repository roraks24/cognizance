class SectorClassifier:
    SECTOR_KEYWORDS = {
        "AI": [
            "ai", "artificial intelligence", "machine learning", "deep learning",
            "llm", "neural", "gpt", "transformer", "nlp", "computer vision",
            "generative", "diffusion", "reinforcement learning", "openai", "anthropic",
            "huggingface", "pytorch", "tensorflow", "ml", "mlops", "vector database"
        ],
        "Fintech": [
            "fintech", "payments", "banking", "crypto", "blockchain", "defi",
            "neobank", "lending", "insurance", "insurtech", "wealth", "trading",
            "robo-advisor", "remittance", "kyc", "aml", "open banking", "embedded finance",
            "stablecoin", "nft", "web3", "wallet", "paytech"
        ],
        "Climate Tech": [
            "climate", "carbon", "renewable", "energy", "solar", "wind", "ev",
            "electric vehicle", "sustainability", "cleantech", "green", "net zero",
            "emissions", "hydrogen", "battery", "grid", "recycling", "circular economy",
            "agritech", "food tech", "water", "biodiversity"
        ],
        "Robotics": [
            "robotics", "robot", "automation", "drone", "autonomous", "actuator",
            "servo", "lidar", "computer vision", "manipulator", "humanoid",
            "warehouse automation", "agv", "cobots", "industrial automation",
            "ros", "embedded systems", "hardware", "mechatronics"
        ],
        "Cybersecurity": [
            "cybersecurity", "security", "encryption", "zero trust", "soc",
            "threat detection", "vulnerability", "pentesting", "siem", "xdr",
            "identity", "iam", "devsecops", "cloud security", "endpoint",
            "ransomware", "phishing", "firewall", "authentication", "biometric"
        ],
        "Health Tech": [
            "health", "healthcare", "medtech", "biotech", "pharma", "telemedicine",
            "digital health", "genomics", "diagnostics", "wearable", "mental health",
            "drug discovery", "clinical trial", "ehr", "patient", "medical device",
            "longevity", "precision medicine", "surgical", "radiology"
        ],
        "DevTools": [
            "devtools", "developer tools", "sdk", "api", "cli", "ide", "platform",
            "infrastructure", "devops", "ci/cd", "kubernetes", "docker", "cloud",
            "observability", "monitoring", "logging", "testing", "deployment",
            "low code", "no code", "developer experience", "dx", "saas"
        ]
    }

    def classify(self, text):
        if not text:
            return None
        text_lower = text.lower()
        scores = {}
        for sector, keywords in self.SECTOR_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                scores[sector] = score
        if not scores:
            return None
        return max(scores, key=scores.get)

    def classify_multi(self, text):
        if not text:
            return []
        text_lower = text.lower()
        results = []
        for sector, keywords in self.SECTOR_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                results.append((sector, score))
        results.sort(key=lambda x: x[1], reverse=True)
        return [s[0] for s in results[:3]]
