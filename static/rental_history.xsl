<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:template match="/">
        <html>
            <head>
                <title>Rental History</title>
                <style>
                    table, th, td {
                        border: 1px solid black;
                        border-collapse: collapse;
                        padding: 8px;
                    }
                    th {
                        background-color: #4CAF50;
                        color: white;
                    }
                </style>
            </head>
            <body>
                <h2>Your Rental History</h2>
                <table>
                    <tr>
                        <th>Car</th>
                        <th>Start Date</th>
                        <th>End Date</th>
                        <th>Total Price ($)</th>
                    </tr>
                    <xsl:for-each select="RentalHistory/Rental">
                        <tr>
                            <td><xsl:value-of select="Car"/></td>
                            <td><xsl:value-of select="StartDate"/></td>
                            <td><xsl:value-of select="EndDate"/></td>
                            <td><xsl:value-of select="TotalPrice"/></td>
                        </tr>
                    </xsl:for-each>
                </table>

                <br/>
                <a href="/account/">
                    <button style="padding: 10px 20px; background-color: #4CAF50; color: white; border: none; border-radius: 5px;">
                        Back to Account
                    </button>
                </a>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
