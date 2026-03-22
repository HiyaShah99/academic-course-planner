const passport = require("passport");
const GoogleStrategy = require("passport-google-oauth20").Strategy;

//Passport Google OAuth2 Strategy
passport.use(new GoogleStrategy({
    clientID: process.env.GOOGLE_CLIENT_ID,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    callbackURL: process.env.GOOGLE_CALLBACK_URL
  },
  function(accessToken, refreshToken, profile, cb) {
    if(profile._json.hd === process.env.UNI_DOMAIN){
      return cb(null, profile._json);
    }else{
      return cb(null, false);
    }
  }
));

passport.serializeUser(function(user, cb){
  cb(null,user);
});
passport.deserializeUser(function(user, cb){
  cb(null, user);
});