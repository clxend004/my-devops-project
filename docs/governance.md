# 📘 Repository Governance Guidelines

## 1. Purpose

This document defines the governance model for the **my-devops-project** repository.  
It ensures structured collaboration, code quality, security, and controlled releases.

---

## 2. Repository Structure

The repository follows a standardized modular structure:
backend/ → Backend service source code

frontend/ → Frontend application

blockchain/ → Smart contracts & blockchain integration

docs/ → Project documentation


This segregation ensures maintainability and separation of concerns.

---

## 3. Branching Strategy

The repository follows a structured branching model.

### Main Branches

#### `main`
- Production-ready code  
- Protected branch  
- No direct commits allowed  

#### `dev`
- Integration branch  
- Feature branches merged here first  

### Feature Branches

**Naming convention:**

- Created from `dev`  
- Merged via Pull Request only  

---

## 4. Pull Request Policy

All changes must follow PR-based workflow:

- ❌ No direct push to `main`  
- ✅ PR required for merging  
- ✅ Minimum 1 approval required  
- ✅ CI pipeline must pass before merge  

This ensures code quality and review validation.

---

## 5. Branch Protection Rules

The following rules are enabled on `main`:

- Require pull request before merging  
- Require status checks to pass (CI)  
- Require at least 1 review approval  
- Prevent force push  
- Prevent branch deletion  

This protects production stability.

---

## 6. Access Control Policy

Access is managed using the **Principle of Least Privilege**:

- **Admin** → Repository owner only  
- **Write** → Contributors  
- **Read** → View-only users  

Only authorized users can modify the repository.

---

## 7. CI/CD Enforcement

The repository integrates **GitHub Actions** for:

- Dependency installation  
- Linting  
- Testing  
- Docker image build validation  

Pull requests cannot be merged if CI checks fail.

---

## 8. Contribution Guidelines

Before contributing:

1. Create feature branch from `dev`  
2. Commit changes with meaningful message  
3. Push branch  
4. Create Pull Request to `dev`  
5. Wait for review & CI success  
6. Merge after approval  

---

## 9. Code Review Standards

Reviewers must verify:

- Code functionality  
- Security practices  
- No hardcoded secrets  
- Proper documentation  
- Passing CI checks  

---

## 10. Governance Compliance

Failure to follow governance rules may result in:

- PR rejection  
- Access revocation  
- Rework requirement  

---

# ✅ Governance Outcome

- ✔ Structured collaboration  
- ✔ Secure repository access  
- ✔ Protected production branch  
- ✔ Controlled merge workflow  
- ✔ Enforced CI validation  
