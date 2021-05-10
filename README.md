# Chat-App-with-Hybrid-Encryption
RSA (Rivest Shamir Adleman) is a publicly used and well-known public key cryptosystem that generates keys using two big and distinct integers. We use Chinese Remainder Theorem (CRT) to improve and fortify the RSA public key cryptosystem algorithm. To add to the system's complexity, the current project generates public/private key pairs with four prime numbers rather than two. To boost protection, the encryption and decryption functions have been revamped to include a special key called encryption key for encryptionand decryption key for decryption, both of which are calculated using the CRT such that they are less reliant on public andprivate key pairs. Here we are using Vigenère cipher concept as well. First in the process of encryption we perform Vigenère cipher encryption by converting the characters into integers for performing mathematical operations on them and then using RSA algorithm with CRT, this is to increase the security and during the decryption first the cipher text is decrypted using RSA with CRT and then Vigenère cipher decryption and then these values are converted back to characters.
With the help of this algorithm a real time web application named Safe Chat is developed using Python Flaskand Socket.IO. With this application users can communicate with each other in the form of messages by creating a chat room, here the message which the sender is sending is sent by encrypting it using the mentioned algorithms and then receiver will see the decrypted data which is the original message.
Home page

![image](https://user-images.githubusercontent.com/59475454/117672444-7be2c700-b1c7-11eb-9988-7fb386932d97.png)

signup

![image](https://user-images.githubusercontent.com/59475454/117673399-65893b00-b1c8-11eb-8155-8af82ff324f4.png)

login

![image](https://user-images.githubusercontent.com/59475454/117673427-6c17b280-b1c8-11eb-8f28-5fd568ccb833.png)

create room

![image](https://user-images.githubusercontent.com/59475454/117673498-776ade00-b1c8-11eb-92d3-44f4e319e0dc.png)

view room

![image](https://user-images.githubusercontent.com/59475454/117673537-805baf80-b1c8-11eb-8ece-2fbc8a2044ee.png)

edit room

![image](https://user-images.githubusercontent.com/59475454/117673575-881b5400-b1c8-11eb-8c24-2905701e6632.png)

Database

![image](https://user-images.githubusercontent.com/59475454/117673676-9c5f5100-b1c8-11eb-9362-1e8446f1f5de.png)


storing messages

![image](https://user-images.githubusercontent.com/59475454/117674116-05df5f80-b1c9-11eb-9c28-b8fb63e82739.png)
