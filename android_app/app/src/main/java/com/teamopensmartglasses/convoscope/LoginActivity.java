/*
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package com.teamopensmartglasses.convoscope;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import androidx.activity.result.ActivityResultLauncher;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.auth.GetTokenResult;
import androidx.activity.result.ActivityResultCallback;
import com.firebase.ui.auth.AuthUI;
import com.firebase.ui.auth.FirebaseAuthUIActivityResultContract;
import com.firebase.ui.auth.IdpResponse;
import com.firebase.ui.auth.data.model.FirebaseAuthUIAuthenticationResult;
import com.google.firebase.auth.ActionCodeSettings;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import com.teamopensmartglasses.convoscope.Config.*;


public class LoginActivity extends AppCompatActivity {
  public final String TAG = "Convoscope_LoginActivity";

  // [START auth_fui_create_launcher]
  // See: https://developer.android.com/training/basics/intents/result
  private final ActivityResultLauncher<Intent> signInLauncher = registerForActivityResult(
          new FirebaseAuthUIActivityResultContract(),
          new ActivityResultCallback<FirebaseAuthUIAuthenticationResult>() {
            @Override
            public void onActivityResult(FirebaseAuthUIAuthenticationResult result) {
              onSignInResult(result);
            }
          }
  );
  // [END auth_fui_create_launcher]

  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_login);
    createSignInIntent();
  }

  public void createSignInIntent() {
    // Choose authentication providers
    List<AuthUI.IdpConfig> providers = Arrays.asList(
            //new AuthUI.IdpConfig.EmailBuilder().build(),
            //new AuthUI.IdpConfig.PhoneBuilder().build(),
            new AuthUI.IdpConfig.GoogleBuilder().build());

    // Create and launch sign-in intent
    Intent signInIntent = AuthUI.getInstance()
            .createSignInIntentBuilder()
            .setAvailableProviders(providers)
            .build();
    signInLauncher.launch(signInIntent);
  }

  private void onSignInResult(FirebaseAuthUIAuthenticationResult result) {
    IdpResponse response = result.getIdpResponse();
    if (result.getResultCode() == RESULT_OK) {
      // Successfully signed in
      FirebaseUser user = FirebaseAuth.getInstance().getCurrentUser();
      Log.d(TAG, "WOAH LOGGED IN");

      // Get the auth token
      if (user != null) {
        user.getIdToken(true)
                .addOnCompleteListener(new OnCompleteListener<GetTokenResult>() {
                  public void onComplete(@NonNull Task<GetTokenResult> task) {
                    if (task.isSuccessful()) {
                      String idToken = task.getResult().getToken();
                      // Use the idToken for your app logic
                      Log.d(TAG, "Auth Token: " + idToken);
                      Config.authToken = "";
                      navigateToMainActivityForSuccess();
                    } else {
                      // Handle error -> task.getException();
                      restartLoginActivity();
                    }
                  }
                });
      }
    } else {
      // Sign in failed. If response is null the user canceled the
      // sign-in flow using the back button. Otherwise check
      // response.getError().getErrorCode() and handle the error.

      restartLoginActivity();

    }
  }
  public void signOut() {
    AuthUI.getInstance()
            .signOut(this)
            .addOnCompleteListener(new OnCompleteListener<Void>() {
              public void onComplete(@NonNull Task<Void> task) {
                Log.d(TAG, "LOGGED OUT");

                // TODO: Evaluate if this is reasonable
                killApp();
              }
            });
  }

  public void delete() {
    AuthUI.getInstance()
            .delete(this)
            .addOnCompleteListener(new OnCompleteListener<Void>() {
              @Override
              public void onComplete(@NonNull Task<Void> task) {
                Log.d(TAG, "AUTH DELETE");

                // TODO: Evaluate if this is reasonable
                killApp();
              }
            });
  }

  public void themeAndLogo() {
    List<AuthUI.IdpConfig> providers = Collections.emptyList();

    // [START auth_fui_theme_logo]
    Intent signInIntent = AuthUI.getInstance()
            .createSignInIntentBuilder()
            .setAvailableProviders(providers)
            .setLogo(com.teamopensmartglasses.smartglassesmanager.R.drawable.elon)      // Set logo drawable
            .setTheme(R.style.AppTheme)      // Set theme
            .build();
    signInLauncher.launch(signInIntent);
    // [END auth_fui_theme_logo]
  }

  public void privacyAndTerms() {
    List<AuthUI.IdpConfig> providers = Collections.emptyList();

    // [START auth_fui_pp_tos]
    Intent signInIntent = AuthUI.getInstance()
            .createSignInIntentBuilder()
            .setAvailableProviders(providers)
            .setTosAndPrivacyPolicyUrls(
                    "https://teamopensmartglasses.com/terms.html",
                    "https://teamopensmartglasses.com/privacy.html")
            .build();
    signInLauncher.launch(signInIntent);
    // [END auth_fui_pp_tos]
  }

  public void emailLink() {
    // [START auth_fui_email_link]
    ActionCodeSettings actionCodeSettings = ActionCodeSettings.newBuilder()
            .setAndroidPackageName(
                    /* yourPackageName= */ "...",
                    /* installIfNotAvailable= */ true,
                    /* minimumVersion= */ null)
            .setHandleCodeInApp(true) // This must be set to true
            .setUrl("https://google.com") // This URL needs to be whitelisted
            .build();

    List<AuthUI.IdpConfig> providers = Arrays.asList(
            new AuthUI.IdpConfig.EmailBuilder()
                    .enableEmailLinkSignIn()
                    .setActionCodeSettings(actionCodeSettings)
                    .build()
    );
    Intent signInIntent = AuthUI.getInstance()
            .createSignInIntentBuilder()
            .setAvailableProviders(providers)
            .build();
    signInLauncher.launch(signInIntent);
    // [END auth_fui_email_link]
  }

  public void catchEmailLink() {
    List<AuthUI.IdpConfig> providers = Collections.emptyList();

    // [START auth_fui_email_link_catch]
    if (AuthUI.canHandleIntent(getIntent())) {
      if (getIntent().getExtras() == null) {
        return;
      }
      String link = getIntent().getExtras().getString("email_link_sign_in");
      if (link != null) {
        Intent signInIntent = AuthUI.getInstance()
                .createSignInIntentBuilder()
                .setEmailLink(link)
                .setAvailableProviders(providers)
                .build();
        signInLauncher.launch(signInIntent);
      }
    }
    // [END auth_fui_email_link_catch]
  }

  public void restartLoginActivity(){
    // Restart the LoginActivity
    Intent intent = new Intent(LoginActivity.this, LoginActivity.class);
    startActivity(intent);
    intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
    finish();
  }

  public void navigateToMainActivityForSuccess(){
    // Navigate back to MainActivity
    Intent intent = new Intent(LoginActivity.this, MainActivity.class);
    startActivity(intent);

    // Optionally, add this if you want to clear the activity stack
    // and prevent the user from returning to the LoginActivity via the back button
    intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
    finish();
  }

  public void killApp(){
    stopService(new Intent(this, ConvoscopeService.class));
    finishAffinity();
    System.exit(0);
  }


//
//  public void setAuthToken(String newAuthToken){
//    SharedPreferences sharedPreferences = getSharedPreferences(appName, MODE_PRIVATE);
//    SharedPreferences.Editor editor = sharedPreferences.edit();
//    editor.putString("authToken", newAuthToken);
//    editor.apply();
//  }
//
//  public String getAuthToken(){
//    SharedPreferences sharedPreferences = getSharedPreferences(appName, MODE_PRIVATE);
//    String value = sharedPreferences.getString("authToken", "");
//    return value;
//  }
}
