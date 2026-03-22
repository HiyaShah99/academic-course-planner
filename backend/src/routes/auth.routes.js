const express = require("express");
const router = express.Router();
const passport = require("passport");
const path = require("path");

//Index route: access the login page
router.get('/',(req,res)=>{
    res.sendFile(path.join(__dirname,"../../../frontend/login/index.html"));
});

//Google auth routes
router.get('/google', passport.authenticate('google', { scope: ['profile', 'email'] }));
router.get('/google/callback', passport.authenticate('google', { failureRedirect: '/auth?error=unauthorized', successRedirect: '/' }));

//Log-out route
router.get('/logout', (req,res)=>{
    req.logOut((err)=>{
        if(err) return next(err);
        req.session.destroy((err)=>{
            if(err) return next(err);
            res.redirect('/auth'); 
        });
    });
});

module.exports = router;