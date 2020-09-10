<h1>Table of contents</h1>

<li>
  <a href="">
    Getting API keys
  </a>
</li>
<li>
  <a href="">
    Configuring the bot
  </a>
</li>
<br>
<br>
<br>
<br>
<br>
<br>

<h1>Obtaining API keys for Twitter & AWS</h1>

First of all, make sure you have an [AWS](https://aws.amazon.com/) account and [Twitter Developer](https://developer.twitter.com/) account. It's fairly simple to get both, just google around if you get stuck!

Next up, navigate to the [S3 console](https://s3.console.aws.amazon.com/s3/home). You will need to create a bucket.

<p align="center">
  <img width=60% src="../cdn/create.png"">
</p>
Fill out the <b>Bucket name</b> and select <i>US East (N. Virginia)</i> as the region. 
<p align="center">
  <img width=60% src="../cdn/name.png"">
</p>

Leave everything as default and keep clicking next until you get to the review screen. Then, press <b>Create Bucket</b>.

<br>




If you did everything correctly, your screen should look something like this:
<p align="center">
  <img width=60% src="../cdn/bucket_done.png"">
</p>
<img src="">

<h2> Setting up API keys</h1>
What you need to do, is create an IAM user, which access keys we will use. Follow
<a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html"> this guide</a>, if you don't know how to go about that!

<br>
<br>
You will need an access key ID and secret access key. Once you get those two keys, fill them out into 'aws.json' file.
<br>
<br>

<h2> Now, setting up Twitter API keys</h1>
You need the Twitter developer account for this one. If you don't know how to obtain the 4 keys needed, follow
<a href="https://themepacific.com/how-to-generate-api-key-consumer-token-access-key-for-twitter-oauth/994/">
This guide</a>!
<br>
<br>

Once you obtain these 4 keys, fill them out in the 'twitter.json' file!

<br>
<br>
