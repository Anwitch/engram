#!/bin/bash

# Engram Skill - Quick Installation Script for Moltbot

set -e

echo "🧠 Engram Skill Installer for Moltbot"
echo "========================================"
echo ""

# Detect skill directory
SKILL_DIR=""
if [ -n "$MOLTBOT_WORKSPACE" ]; then
    SKILL_DIR="$MOLTBOT_WORKSPACE/skills/engram"
    echo "📁 Installing to agent workspace: $SKILL_DIR"
elif [ -d "$HOME/.clawdbot" ]; then
    SKILL_DIR="$HOME/.clawdbot/skills/engram"
    echo "📁 Installing to shared skills: $SKILL_DIR"
else
    echo "❌ Error: Cannot find Moltbot installation"
    echo "   Please set MOLTBOT_WORKSPACE or ensure ~/.clawdbot exists"
    exit 1
fi

# Create skills directory if needed
mkdir -p "$(dirname "$SKILL_DIR")"

# File copy skipped - skill is already in place

# Check and install system dependencies
echo ""
echo "🔍 Checking system dependencies..."

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed"
    echo "   Please install python3 first"
    exit 1
fi

# Check if python3-venv is available, install if needed
if ! python3 -m venv --help &> /dev/null; then
    echo "📦 python3-venv not found. Installing system dependencies..."
    
    # Detect OS and install appropriate package
    if command -v apt-get &> /dev/null; then
        echo "   - Detected Debian/Ubuntu system"
        echo "   - Running: sudo apt-get update && sudo apt-get install -y python3-venv python3-pip"
        sudo apt-get update && sudo apt-get install -y python3-venv python3-pip
    elif command -v yum &> /dev/null; then
        echo "   - Detected RHEL/CentOS system"
        echo "   - Running: sudo yum install -y python3-venv python3-pip"
        sudo yum install -y python3-venv python3-pip
    elif command -v dnf &> /dev/null; then
        echo "   - Detected Fedora system"
        echo "   - Running: sudo dnf install -y python3-venv python3-pip"
        sudo dnf install -y python3-venv python3-pip
    else
        echo "❌ Error: Could not detect package manager"
        echo "   Please manually install python3-venv and python3-pip for your system"
        exit 1
    fi
    
    echo "   ✅ System dependencies installed"
else
    echo "   ✅ python3-venv already available"
fi

# Install Python dependencies
echo ""
echo "🐍 Installing Python dependencies into a virtual environment..."
VENV_DIR="$SKILL_DIR/.venv"

# Remove old venv if it exists but is broken
if [ -d "$VENV_DIR" ] && [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo "   - Removing broken virtual environment..."
    rm -rf "$VENV_DIR"
fi

if [ ! -d "$VENV_DIR" ]; then
    echo "   - Creating new virtual environment in $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
    
    # Verify venv was created successfully
    if [ ! -f "$VENV_DIR/bin/activate" ]; then
        echo "❌ Error: Failed to create virtual environment"
        echo "   Please check that python3-venv is properly installed"
        exit 1
    fi
    echo "   - Virtual environment created successfully"
else
    echo "   - Using existing virtual environment"
fi

echo "   - Installing packages..."

# Check if requirements.txt exists
if [ ! -f "$SKILL_DIR/requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found at $SKILL_DIR/requirements.txt"
    exit 1
fi

source "$VENV_DIR/bin/activate"
pip install -q -r "$SKILL_DIR/requirements.txt"

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install Python dependencies"
    deactivate
    exit 1
fi

deactivate
echo "   - Dependencies installed."

# Make script executable
chmod +x "$SKILL_DIR/tool_engram_search.py"

echo ""
echo "✅ Installation complete!"
echo ""
echo "📝 Next steps:"
echo ""
echo "1. Configure your API keys in ~/.clawdbot/moltbot.json:"
echo ""
echo '   {
     "skills": {
       "entries": {
         "engram": {
           "enabled": true,
           "env": {
             "GEMINI_API_KEY": "your_key_here",
             "PINECONE_API_KEY": "your_key_here",
             "PINECONE_HOST": "https://your-index.svc.pinecone.io"
           }
         }
       }
     }
   }'
echo ""
echo "2. Get your API keys:"
echo "   - Gemini: https://aistudio.google.com/app/apikey"
echo "   - Pinecone: https://app.pinecone.io/"
echo ""
echo "3. Verify installation:"
echo "   moltbot skills"
echo ""
echo "4. Test in a new session:"
echo '   "Search my notes for embeddings"'
echo ""
echo "📚 See README.md for detailed documentation"
echo ""
