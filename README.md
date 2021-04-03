# Spotify Collaborative Playlists through Github + GH Actions

This repository can be used as template repository to manage Spotify public playlists through Github, using Github Actions.
By using Github, the playlists can be both public and collaborative, using Issues and Pull Requests to collaborate.

The Github Actions included on the repository, with the Python app bundled, can:

- Dump a Spotify playlist into the repository
- Add and delete tracks from the playlist (currently does not support rearranging existing items, nor append new tracks in between the playlist)

**This project is experimental and might have undesirable effects. Use it under your responsability!**

## Playlists using this template

- [Sample/Test Playlist](https://github.com/David-Lor/Spotify-Collaborative-Public-Playlists-Test)

## Usage

### a) Setup the repository

0. Use this Template Repository to create a new repository for you playlist (one repository can only manage one playlist).
1. Create a new app in [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
2. Edit the app and add `http://localhost` in "Redirect URIs".
3. Open in your browser `https://accounts.spotify.com/authorize?response_type=code&client_id={app client id}&scope=playlist-modify-public&redirect_uri=http%3A%2F%2Flocalhost`; copy the "code" param from the redirected url (everything after `https://localhost/?code=`). If you want to allow modifying private playlists as well, you should use the URL ``https://accounts.spotify.com/authorize?response_type=code&client_id={app client id}&scope=playlist-modify-public%20playlist-modify-private&redirect_uri=http%3A%2F%2Flocalhost`` instead.
4. Create a new Github Personal Access Token from Settings > Developer settings > Personal access tokens. Requires a scope of "public_repo", or the whole "repo" if the playlist repository is private. Copy this token for the next step.
5. Set the following Secrets on the Github repository settings:
   - `SPOTIFY_CLIENT_ID`: app client id
   - `SPOTIFY_CLIENT_SECRET`: app client secret
   - `SPOTIFY_AUTHORIZATION_CODE`: code returned in step 3
   - `SPOTIFY_PLAYLIST_ID`: id of Spotify playlist to use. This can be acquired from Spotify, right click on the playlist > Share > Copy playlist link. You'd get something like `https://open.spotify.com/playlist/08OgybZ7enLqMROCIi3cg8?si=0470048b5c0548bf`; copy the ID after the `/playlist/` and before the extra params (`?...`). In this example, the ID would be `08OgybZ7enLqMROCIi3cg8`
   - `GH_TOKEN`: Personal Access Token created in step 4.
6. Launch the Initial Login workflow: on the playlist repository, go to Actions > Workflows: Initial Login > Run workflow. You must complete this step in less than 1 hour after acquiring the Authorization Code in step 3. After successfully logging in, the `GH_TOKEN` can be revoked.
7. Pull the Spotify Playlist into the repository, launching the Pull Playlist workflow: on the playlist repository, go to Actions > Workflows: Pull Playlist > Run workflow

To restart the authentication process (login again), repeat steps 3, 5, 6.

### b) Add/delete/alter songs

8. Edit the template.tsv file. This file is like a table, where each line (row) represents a song, and each column represents one data from it. Columns are split by tabulations.
   - **New songs:** add a new line with the ID of a Spotify song. You can obtain it from Spotify: right click on a song > Share > Copy song link.
     You'd get something like `https://open.spotify.com/track/6sgVx9J04tBP7eJDLLNwz5?si=52af930451534801`. Copy the ID after the `/track/` and before the extra params (`?...`). In this example, the ID would be `6sgVx9J04tBP7eJDLLNwz5`.
     The song details (name, album, author) is acquired by the workflows, so you don't need to complete that info.
     You can write an additional description after the ID, split by a tab.
   - **Delete songs:** just remove the line with the song you want to remove.
   - **Add description to an existing song:** write it at the end of the line of the song. If no description currently exists, the line will end with a tab: write the description after it.
9. Run the Push Playlist workflow.

## Warnings

A playlist can be altered from both Spotify and Github, but when doing this, must be careful with possible conflicts.
You could find a scenario where you:

1. pull from Spotify to Github
2. add a song A on Spotify
3. add a song B on the Github repository
4. push changes from Github to Spotify

In this case, the song A would dissapear, since it's not on the playlist file. To avoid this, changes made on Spotify should be pulled to the repository before pushing any changes to Spotify.
You can also configure the playlist_pull workflow to periodically pull the playlist using [schedule](https://docs.github.com/en/actions/reference/events-that-trigger-workflows#schedule).

## Changelog

- 0.1
   - Initial functional version, featuring Add and Delete songs; Pull and Push playlist between Spotify and Github

## TODO

- Allow reordering playlist from Github
- Add workflow to update child repositories with changes from the Template repository
