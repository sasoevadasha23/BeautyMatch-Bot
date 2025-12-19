echo "Настройка базы данных PostgreSQL"
CURRENT_USER=$(whoami)
psql -U "$CURRENT_USER" -d postgres -c "CREATE DATABASE makeup_bot;" 2>/dev/null || echo "База данных уже существует или ошибка создания"


