echo 'start creating certificate files'
echo 'pwd: $(pwd)'

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout cert.key -out cert.crt

echo 'start chmod'

chmod 644 cert.crt
chmod 600 cert.key


