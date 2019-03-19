const path = require('path');
const webpack = require('webpack');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const ManifestRevisionPlugin = require('manifest-revision-webpack-plugin');

var config = {
    entry: {
        main: path.resolve(__dirname, 'b_io/assets/scripts/index.js')
    },
    output: {
        filename: '[name].js',
        path: path.resolve(__dirname, 'b_io/static/'),
        publicPath: 'http://127.0.0.1:3000/static/'
    },
    devServer: {
        host: '127.0.0.1',
        port: 3000,
        hot: true,
        index: '',
        headers: {
            "Access-Control-Allow-Origin": "http://127.0.0.1:8080",
        },
        proxy: {
            context: () => true,
            target: 'http://127.0.0.1:8080'
        }
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader"
                }
            },
            {
                test: /\.css$/,
                use: [
                    "style-loader",
                    "css-loader"
                ]
            },
            {
                test: /\.scss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    "css-loader",
                    "postcss-loader",
                    "sass-loader"
                ]
            },
            {
                test: /\.(gif|png|jpe?g|svg)$/i,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            name: '[name].[hash].[ext]'
                        }
                    },
                    {
                        loader: 'image-webpack-loader',
                        options: {
                            disable: true,
                        },
                    }
                ]
            },
            {
                test: /\.(ttf|eot|woff|woff2)$/i,
                use: {
                    loader: "file-loader",
                    options: {
                        name: "[name].[hash].[ext]",
                    },
                },
            },
        ]
    },
    plugins: [
        new ManifestRevisionPlugin(
            path.resolve(__dirname, 'b_io/static/manifest.json'), {
                rootAssetPath: path.resolve(__dirname, 'b_io/assets/'),
                extensionsRegex: /\.(gif|png|jpe?g|svg|ttf|eot|woff|woff2)$/i
            }
        ),
    ]
};

module.exports = (env, argv) => {

    if (argv.mode === 'development') {
        // config.devtool = 'source-map';
        config.plugins.push(
            new webpack.HotModuleReplacementPlugin()
        );
        config.plugins.push(
            new MiniCssExtractPlugin({
                filename: "[name].css",
                chunkFilename: "[id].css"
            })
        );
    }

    if (argv.mode === 'production') {
        config.output.filename = '[name]-[hash].js';
        config.output.publicPath = '/static/';
        config.plugins.push(
            new MiniCssExtractPlugin({
                filename: "[name]-[hash].css",
                chunkFilename: "[id]-[hash].css"
            })
        );
    }

    return config;
};
