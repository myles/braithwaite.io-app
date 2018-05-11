'use strict';

var path = require('path'),
    gulp = require('gulp'),
    sass = require('gulp-sass'),
    runSequence = require('run-sequence'),
    browserSync = require('browser-sync'),
    rename = require("gulp-rename"),
    babel = require('gulp-babel'),
    imagemin = require('gulp-imagemin'),
    sourcemaps = require('gulp-sourcemaps'),
    ttf2woff2 = require('gulp-ttf2woff2'),
    ttf2woff = require('gulp-ttf2woff'),
    ttf2eot = require('gulp-ttf2eot'),
    git = require('gulp-git'),
    env = require('gulp-env'),
    spawn = require('child_process').spawn,
    reload = browserSync.reload;

function bioConfig() {
  var app_dir = path.join(__dirname, 'b_io');

  return {
    srcFonts: path.join(app_dir, 'assets', 'fonts'),
    destFonts: path.join(app_dir, 'static', 'fonts'),

    srcScripts: path.join(app_dir, 'assets', 'scripts'),
    destScripts: path.join(app_dir, 'static'),

    srcStyles: path.join(app_dir, 'assets', 'styles'),
    destStyles: path.join(app_dir, 'static'),

    srcImages: path.join(app_dir, 'assets', 'images'),
    destImages: path.join(app_dir, 'static'),

    templates: path.join(app_dir, 'templates'),

    devPort: 5000
  }
}

var b_io = bioConfig();

gulp.task('styles', function() {
  gulp.src(path.join(b_io.srcStyles, 'index.scss'))
      .pipe(sourcemaps.init())
      .pipe(sass({
        includePaths: ['node_modules/']
      }).on('error', sass.logError))
      .pipe(sourcemaps.write())
      .pipe(rename('style.css'))
      .pipe(gulp.dest(b_io.destStyles))
      .pipe(reload({ stream: true }));
});

gulp.task('scripts', function() {
  gulp.src(path.join(b_io.srcScripts, 'index.js'))
      .pipe(sourcemaps.init())
      .pipe(babel({
        presets: ['env'],
        plugins: ['add-module-exports']
      }))
      .pipe(sourcemaps.write())
      .pipe(rename('script.js'))
      .pipe(gulp.dest(b_io.destScripts))
      .pipe(reload({ stream: true }));
});

gulp.task('fonts', function() {
  gulp.src(path.join(b_io.srcFonts, '*.ttf'))
      .pipe(ttf2woff2())
      .pipe(gulp.dest(b_io.destFonts));

  gulp.src(path.join(b_io.srcFonts, '*.ttf'))
      .pipe(ttf2eot())
      .pipe(gulp.dest(b_io.destFonts));

  gulp.src(path.join(b_io.srcFonts, '*.ttf'))
      .pipe(ttf2woff())
      .pipe(gulp.dest(b_io.destFonts));
});

gulp.task('images', function() {
  gulp.src(path.join(b_io.srcImages, '*'))
      .pipe(imagemin())
      .pipe(gulp.dest(b_io.destImages));
});

gulp.task('build', ['styles', 'scripts', 'fonts', 'images']);

gulp.task('browserSync', ['build'], function() {
  browserSync.init([
    `${b_io.destStyles}/**/*.css`,
    `${b_io.destScripts}/**/*.js`
  ], {
    proxy: '127.0.0.1:5000'
  });
});

gulp.task('watch', function() {
  gulp.watch(`${b_io.srcStyles}/**/*.scss`, ['styles']).on('change', reload);
  gulp.watch(`${b_io.srcScripts}/**/*.js`, ['scripts']).on('change', reload);
  gulp.watch(`${b_io.srcImages}/**/*`, ['images']).on('change', reload);
});

gulp.task('flaskRun', function(cb) {
  var cmd = spawn('pipenv', ['run', 'flask', 'run', '--port', b_io.devPort], {
    stdio: 'inherit'
  });

  cmd.on('close', function(code) {
    console.log(`flaskRun exited with code ${code}`);
    cb(code);
  });
});

gulp.task('flaskFreeze', function(cb) {
  var cmd = spawn('pipenv', ['run', 'flask', 'freeze'], {
    stdio: 'inherit'
  });

  cmd.on('close', function(code) {
    console.log(`flaskFreeze exited with code ${code}`);
    cb(code);
  });
});

gulp.task('flaskFreezeNetlify', function(cb) {
  var cmd = spawn('flask', ['freeze'], {
    stdio: 'inherit'
  });

  cmd.on('close', function(code) {
    console.log(`flaskFreeze exited with code ${code}`);
    cb(code);
  });
});

gulp.task('awsS3Sync', function(cb) {
  var cmd = spawn('aws', ['s3', 'sync', './build/', 's3://braithwaite.io', '--exclude', '.DS_Store', '--acl', 'public-read'], {
    stdio: 'inherit'
  });

  cmd.on('close', function(code) {
    console.log(`deploy exited with code ${code}`);
    cb(code);
  });
});

gulp.task('cloneNotebooks', function() {
  git.clone('https://github.com/myles/braithwaite.io.git', { args: './notebooks/' }, function(err) {
    if (err) throw err;
  })
});

gulp.task('set-env', function() {
  env({
    vars: {
      FLASK_APP: 'autoapp.py'
    }
  })
});

gulp.task('runServer', function() {
  runSequence(['build'], ['flaskRun', 'browserSync', 'watch']);
});

gulp.task('deploy', ['build', 'flaskFreeze', 'awsS3Sync']);

gulp.task('default', ['build', 'flaskFreeze']);
