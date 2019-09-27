package com.bigdatasystems;

public class SentimentClassification {
    /*
     * "Very negative" = 0
     * "Negative" = 1
     * "Neutral" = 2
     * "Positive" = 3
     * "Very positive" = 4
     */

    int veryPositive;
    int positive;
    int neutral;
    int negative;
    int veryNegative;

    public int getVeryPositive() {
        return veryPositive;
    }

    public void setVeryPositive(int veryPositive) {
        this.veryPositive = veryPositive;
    }

    public int getPositive() {
        return positive;
    }

    public void setPositive(int positive) {
        this.positive = positive;
    }

    public int getNeutral() {
        return neutral;
    }

    public void setNeutral(int neutral) {
        this.neutral = neutral;
    }

    public int getNegative() {
        return negative;
    }

    public void setNegative(int negative) {
        this.negative = negative;
    }

    public int getVeryNegative() {
        return veryNegative;
    }

    public void setVeryNegative(int veryNegative) {
        this.veryNegative = veryNegative;
    }
}