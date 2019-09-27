package com.bigdatasystems;

import org.apache.log4j.BasicConfigurator;
import java.sql.*;

public class Main {

    public static void main(String[] args) {
        analyseReviews();
    }

    public static void analyseReviews() {
        BasicConfigurator.configure();

        SentimentAnalyzer sentimentAnalyzer = new SentimentAnalyzer();
        sentimentAnalyzer.initialize();
        try {

            //Class.forName("com.mysql.cj.jdbc.Driver");
            Connection conn = DriverManager.getConnection(
                    "jdbc:mysql://localhost:3306/AllReviews","kajal","");
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT DISTINCT review_text FROM TABLE_REVIEWS ORDER BY LENGTH(review_text)"); // LIMIT 50

            int distinctReviewsSoFar = 0;
            long startTime = System.currentTimeMillis();

            while (rs.next()) {
                String currentReview = rs.getString(1);
                SentimentResult sentimentResult = sentimentAnalyzer.getSentimentResult(currentReview);
                String sentimentType = sentimentResult.getSentimentType();
                int sentimentScore = sentimentResult.getSentimentScore();

                //System.out.println(currentReview + " : " + sentimentType);

                distinctReviewsSoFar++;
                if (distinctReviewsSoFar % 100 == 0) {
                    System.out.println("Distinct reviews so far: " + distinctReviewsSoFar);
                }

                if (currentReview != null && !currentReview.isEmpty() && sentimentType != null && !sentimentType.isEmpty()) {

                    String query = "UPDATE TABLE_REVIEWS SET review_sentiment = ? WHERE review_text = ?;";
                    PreparedStatement preparedStmt = conn.prepareStatement(query);
                    preparedStmt.setString(1, sentimentType);
                    preparedStmt.setString(2, currentReview);

                    // execute the java prepared statement
                    preparedStmt.executeUpdate();

                    //System.out.println(preparedStmt.toString());
                }
            }
            long estimatedTime = System.currentTimeMillis() - startTime;
            System.out.println("Time elapsed: " + estimatedTime/1000 + " seconds");
            conn.close();

        } catch (Exception e) {
            System.out.println("Exception caught: " + e);
        }
    }
}